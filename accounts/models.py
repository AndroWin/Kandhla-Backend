"""
Republic of Kandhla - Custom User Model
SCHEMA.md ke mutabiq: accounts_user table with UUID PK,
Google Login, Device ID binding, RBAC roles, Credibility Score,
3-Strike moderation system, aur Mohalla/City association.
"""

import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    """
    Custom User Manager - Google Login based hai toh password optional hai.
    Email + Google ID se user create hota hai.
    """

    def create_user(self, email, name, google_id=None, apple_id=None, **extra_fields):
        """Normal citizen user create karo."""
        if not email:
            raise ValueError('Email address zaroori hai.')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            name=name,
            google_id=google_id,
            apple_id=apple_id,
            **extra_fields,
        )
        # Google login based hai, password set nahi hota normally
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        """Django admin superuser create karo."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.Role.SUPREME_MINISTER)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser ke liye is_staff=True hona chahiye.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser ke liye is_superuser=True hona chahiye.')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User Model for Republic of Kandhla.
    SCHEMA.md: accounts_user table
    - UUID primary key
    - Google ID + Device ID binding (anti-fraud voting)
    - Role-Based Access Control (citizen, mohalla_minister, city_minister, supreme_minister)
    - Credibility Score system
    - 3-Strike moderation system with timed bans
    """

    class Role(models.TextChoices):
        CITIZEN = 'citizen', 'Citizen'
        MOHALLA_MINISTER = 'mohalla_minister', 'Mohalla Minister'
        CITY_MINISTER = 'city_minister', 'City Minister'
        SUPREME_MINISTER = 'supreme_minister', 'Supreme Minister'

    # Primary Key - UUID (SCHEMA.md ke mutabiq)
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='User ID',
    )

    # Google Authentication Fields
    google_id = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
        verbose_name='Google ID',
        help_text='Google OAuth unique identifier',
    )
    
    # Apple Authentication Fields
    apple_id = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
        verbose_name='Apple ID',
        help_text='Apple Sign-In unique identifier',
    )

    # Device ID Binding - Anti-fraud voting ke liye
    # REQUIREMENTS.md: "Every vote and active session is bound to the physical device ID"
    device_id = models.CharField(
        max_length=255,
        blank=True,
        default='',
        db_index=True,
        verbose_name='Device ID',
        help_text='Physical device identifier for anti-fraud voting',
    )

    # Basic Profile Fields
    email = models.EmailField(
        unique=True,
        verbose_name='Email Address',
    )
    name = models.CharField(
        max_length=150,
        verbose_name='Full Name',
    )
    avatar_url = models.URLField(
        max_length=500,
        blank=True,
        default='',
        verbose_name='Avatar URL',
        help_text='Google profile picture URL',
    )

    # City & Mohalla Association
    # REQUIREMENTS.md: "Users select their City and Mohalla during profile creation"
    city = models.ForeignKey(
        'ecosystem.City',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='citizens',
        verbose_name='City',
    )
    mohalla = models.ForeignKey(
        'ecosystem.Mohalla',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='residents',
        verbose_name='Mohalla',
    )

    # RBAC Role System
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CITIZEN,
        verbose_name='Role',
        help_text='User role for RBAC permissions',
    )

    # Credibility Score System
    # REQUIREMENTS.md: "Requires minimum Credibility Score" for nominations
    credibility_score = models.IntegerField(
        default=100,
        verbose_name='Credibility Score',
        help_text='Reputation score — nomination ke liye minimum 500 chahiye',
    )

    # 3-Strike Moderation System
    # REQUIREMENTS.md: 6hr -> 24hr -> 72hr -> Permanent Ban
    strike_count = models.IntegerField(
        default=0,
        verbose_name='Strike Count',
        help_text='Moderation strikes — 4th strike = permanent ban',
    )
    ban_until = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Banned Until',
        help_text='Timestamp tak user banned hai. Null = not banned.',
    )

    # Status Fields
    is_active = models.BooleanField(
        default=True,
        verbose_name='Active',
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='Staff Status',
        help_text='Django admin access ke liye.',
    )

    # Timestamps
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Created At',
    )

    # Manager
    objects = UserManager()

    # Auth config
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        db_table = 'accounts_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['google_id'], name='idx_user_google_id'),
            models.Index(fields=['device_id'], name='idx_user_device_id'),
            models.Index(fields=['city', 'mohalla'], name='idx_user_city_mohalla'),
            models.Index(fields=['role'], name='idx_user_role'),
            models.Index(fields=['credibility_score'], name='idx_user_credibility'),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_role_display()}) - {self.email}"

    @property
    def is_banned(self):
        """Check karo ki user currently banned hai ya nahi."""
        if self.strike_count >= 4:
            return True  # Permanent ban
        if self.ban_until and self.ban_until > timezone.now():
            return True
        return False

    @property
    def is_minister(self):
        """Check karo ki user kisi bhi level ka minister hai."""
        return self.role in (
            self.Role.MOHALLA_MINISTER,
            self.Role.CITY_MINISTER,
            self.Role.SUPREME_MINISTER,
        )

    @property
    def can_nominate(self):
        """Check karo ki user election nomination ke eligible hai (Credibility >= 500)."""
        return self.credibility_score >= 500 and not self.is_banned
