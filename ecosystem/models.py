"""
Republic of Kandhla - Ecosystem Models
SCHEMA.md ke mutabiq: City, Mohalla, MohallaChangeRequest, Cabinet tables.
Ye models poore political ecosystem ki foundation hain.
"""

import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone


class City(models.Model):
    """
    City Model — Republic ka base entity.
    SCHEMA.md: ecosystem_city table
    - Ek city = ek independent republic (e.g., "Kandhla")
    - Samvidhan (Constitution) HTML content Admin se manage hota hai
    - Code of Conduct toggle for elections
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='City ID',
    )
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='City Name',
        help_text='City ka naam — e.g., "Kandhla"',
    )
    state = models.CharField(
        max_length=100,
        verbose_name='State',
        help_text='State jismein city hai — e.g., "Uttar Pradesh"',
    )
    samvidhan_content = models.TextField(
        blank=True,
        default='',
        verbose_name='Samvidhan (Constitution)',
        help_text='City ki Samvidhan ka HTML/RichText content — Django Admin se manage hota hai',
    )
    is_code_of_conduct_active = models.BooleanField(
        default=False,
        verbose_name='Achaar Sanhita Active',
        help_text='Jab True ho, posting disabled ho jati hai (Election ke dauran)',
    )

    class Meta:
        db_table = 'ecosystem_city'
        verbose_name = 'City'
        verbose_name_plural = 'Cities'
        ordering = ['name']

    def __str__(self):
        return f"{self.name}, {self.state}"


class Mohalla(models.Model):
    """
    Mohalla Model — City ke andar micro-constituency.
    SCHEMA.md: ecosystem_mohalla table
    - Har mohalla ek city se linked hai
    - Mohalla election alag se hoti hai (monthly)
    - Population count tracked hota hai
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='Mohalla ID',
    )
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name='mohallas',
        verbose_name='City',
    )
    name = models.CharField(
        max_length=150,
        verbose_name='Mohalla Name',
        help_text='Mohalla ka naam — e.g., "Mohalla Qazi Sarai"',
    )
    population_count = models.IntegerField(
        default=0,
        verbose_name='Population Count',
        help_text='Registered users ki total count is mohalla mein',
    )

    class Meta:
        db_table = 'ecosystem_mohalla'
        verbose_name = 'Mohalla'
        verbose_name_plural = 'Mohallas'
        ordering = ['city', 'name']
        unique_together = [['city', 'name']]
        indexes = [
            models.Index(fields=['city'], name='idx_mohalla_city'),
        ]

    def __str__(self):
        return f"{self.name} ({self.city.name})"


class MohallaChangeRequest(models.Model):
    """
    Mohalla Change Request Model.
    SCHEMA.md: ecosystem_mohallarequest table
    REQUIREMENTS.md: "Users cannot change their Mohalla manually once set.
    To change, they must submit a Mohalla Change Request which the Django Admin must approve.
    All requests freeze automatically when an election date is announced."
    """

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='Request ID',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mohalla_change_requests',
        verbose_name='User',
    )
    target_mohalla = models.ForeignKey(
        Mohalla,
        on_delete=models.CASCADE,
        related_name='incoming_requests',
        verbose_name='Target Mohalla',
        help_text='Jis mohalla mein jaana chahta hai',
    )
    reason = models.TextField(
        verbose_name='Reason',
        help_text='Mohalla change karne ki wajah',
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name='Status',
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Created At',
    )

    class Meta:
        db_table = 'ecosystem_mohallarequest'
        verbose_name = 'Mohalla Change Request'
        verbose_name_plural = 'Mohalla Change Requests'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status'], name='idx_mohallareq_user_status'),
        ]

    def __str__(self):
        return f"{self.user.name} → {self.target_mohalla.name} ({self.get_status_display()})"


class Cabinet(models.Model):
    """
    Cabinet Model — Elected leaders ki team.
    SCHEMA.md: ecosystem_cabinet table
    REQUIREMENTS.md:
    - Supreme Minister -> max 11 members (City Cabinet)
    - Mohalla Minister -> max 5 members (Mohalla Cabinet)
    - Har member ka ek department aur ruby color badge hota hai
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='Cabinet Entry ID',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cabinet_positions',
        verbose_name='Cabinet Member',
    )
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='city_cabinet',
        verbose_name='City',
        help_text='City level cabinet ke liye (Supreme Minister ki team)',
    )
    mohalla = models.ForeignKey(
        Mohalla,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='mohalla_cabinet',
        verbose_name='Mohalla',
        help_text='Mohalla level cabinet ke liye (Mohalla Minister ki team)',
    )
    department_name = models.CharField(
        max_length=100,
        verbose_name='Department',
        help_text='Department ka naam — e.g., "Home Minister", "Infra Head"',
    )
    ruby_color = models.CharField(
        max_length=30,
        verbose_name='Ruby Badge Color',
        help_text='VIP badge ka color — e.g., "violet", "grey"',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Active',
    )

    class Meta:
        db_table = 'ecosystem_cabinet'
        verbose_name = 'Cabinet Member'
        verbose_name_plural = 'Cabinet Members'
        ordering = ['city', 'mohalla', 'department_name']
        indexes = [
            models.Index(fields=['city', 'is_active'], name='idx_cabinet_city_active'),
            models.Index(fields=['mohalla', 'is_active'], name='idx_cabinet_mohalla_active'),
        ]

    def __str__(self):
        location = self.city.name if self.city else self.mohalla.name if self.mohalla else 'Unknown'
        return f"{self.user.name} - {self.department_name} ({location})"
