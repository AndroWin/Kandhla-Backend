"""
Republic of Kandhla - Content Models
SCHEMA.md ke mutabiq: Post aur Concern tables.
Feed system, announcements, ads, anonymous posts, aur Samasya (Concern) reporting.
"""

import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone


class Post(models.Model):
    """
    Post Model — Mohalla feed ka core content.
    SCHEMA.md: content_post table
    REQUIREMENTS.md:
    - Content Types: Text, Photos (Videos disabled)
    - Post types: normal, announcement (admin pinned), ad (local business), official_order (minister)
    - Anonymous posting option (Whistleblower feature)
    - Cross-Mohalla: dekh sakte hain, Like/Dislike kar sakte hain, but Comment BLOCKED
    """

    class PostType(models.TextChoices):
        NORMAL = 'normal', 'Normal Post'
        ANNOUNCEMENT = 'announcement', 'Announcement (Pinned)'
        AD = 'ad', 'Advertisement'
        OFFICIAL_ORDER = 'official_order', 'Official Order'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='Post ID',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Author',
    )
    mohalla = models.ForeignKey(
        'ecosystem.Mohalla',
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Mohalla',
        help_text='Jis mohalla mein ye post dikhegi',
    )
    content_text = models.TextField(
        blank=True,
        null=True,
        verbose_name='Content Text',
    )
    image_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name='Image URL',
        help_text='Post ki image (Videos disabled to save storage)',
    )
    post_type = models.CharField(
        max_length=20,
        choices=PostType.choices,
        default=PostType.NORMAL,
        verbose_name='Post Type',
    )
    is_anonymous = models.BooleanField(
        default=False,
        verbose_name='Anonymous Post',
        help_text='True = Whistleblower anonymous post (public ko anonymous dikhega, Admin/SM track kar sakta hai)',
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Created At',
    )

    class Meta:
        db_table = 'content_post'
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['mohalla', '-created_at'], name='idx_post_mohalla_date'),
            models.Index(fields=['user'], name='idx_post_user'),
            models.Index(fields=['post_type'], name='idx_post_type'),
        ]

    def __str__(self):
        author = 'Anonymous' if self.is_anonymous else self.user.name
        text_preview = (self.content_text[:50] + '...') if self.content_text and len(self.content_text) > 50 else (self.content_text or '[Image Post]')
        return f"{author}: {text_preview}"


class Concern(models.Model):
    """
    Concern (Samasya) Model — Citizens ki local issues reporting.
    SCHEMA.md: content_concern table
    REQUIREMENTS.md:
    - Users raise issues with images and details
    - Other users vote via Support / Do Not Support
    - High support increases author's Credibility Score
    - Status flow: pending → city_priority → resolved
    """

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CITY_PRIORITY = 'city_priority', 'City Priority'
        RESOLVED = 'resolved', 'Resolved'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='Concern ID',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='concerns',
        verbose_name='Raised By',
    )
    mohalla = models.ForeignKey(
        'ecosystem.Mohalla',
        on_delete=models.CASCADE,
        related_name='concerns',
        verbose_name='Mohalla',
    )
    image_url = models.URLField(
        max_length=500,
        verbose_name='Image URL',
        help_text='Concern ki supporting image (zaroori hai)',
    )
    description = models.TextField(
        verbose_name='Description',
        help_text='Issue ki detailed description',
    )
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name='Status',
    )
    support_count = models.IntegerField(
        default=0,
        verbose_name='Support Count',
        help_text='Kitne logon ne Support kiya',
    )
    do_not_support_count = models.IntegerField(
        default=0,
        verbose_name='Do Not Support Count',
        help_text='Kitne logon ne Do Not Support kiya',
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Created At',
    )

    class Meta:
        db_table = 'content_concern'
        verbose_name = 'Concern (Samasya)'
        verbose_name_plural = 'Concerns (Samasya)'
        ordering = ['-support_count', '-created_at']
        indexes = [
            models.Index(fields=['mohalla', 'status'], name='idx_concern_mohalla_status'),
            models.Index(fields=['user'], name='idx_concern_user'),
            models.Index(fields=['-support_count'], name='idx_concern_support'),
        ]

    def __str__(self):
        desc_preview = (self.description[:60] + '...') if len(self.description) > 60 else self.description
        return f"[{self.get_status_display()}] {desc_preview}"

    @property
    def net_support(self):
        """Net support score = Support - Do Not Support."""
        return self.support_count - self.do_not_support_count
