"""
Republic of Kandhla - Accounts Admin Configuration
Django Admin panel mein User model ka detailed management.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom User Admin - RBAC roles, Credibility Score, Strike system,
    aur Device ID tracking ke saath full admin control.
    """

    list_display = (
        'name',
        'email',
        'role',
        'city',
        'mohalla',
        'credibility_score',
        'strike_count',
        'is_active',
        'is_banned',
        'created_at',
    )
    list_filter = (
        'role',
        'is_active',
        'is_staff',
        'city',
        'strike_count',
    )
    search_fields = (
        'name',
        'email',
        'google_id',
        'device_id',
    )
    ordering = ('-created_at',)
    readonly_fields = ('id', 'google_id', 'created_at',)

    fieldsets = (
        ('Basic Info', {
            'fields': ('id', 'email', 'name', 'avatar_url', 'google_id', 'device_id'),
        }),
        ('Location', {
            'fields': ('city', 'mohalla'),
        }),
        ('Role & Permissions', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Credibility & Moderation', {
            'fields': ('credibility_score', 'strike_count', 'ban_until'),
            'description': '3-Strike Rule: 6hr → 24hr → 72hr → Permanent Ban',
        }),
        ('Timestamps', {
            'fields': ('created_at',),
        }),
    )

    add_fieldsets = (
        ('Create New User', {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'role', 'city', 'mohalla'),
        }),
    )

    def is_banned(self, obj):
        """Admin list mein banned status dikhao."""
        return obj.is_banned
    is_banned.boolean = True
    is_banned.short_description = 'Banned?'
