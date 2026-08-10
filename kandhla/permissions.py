"""
Republic of Kandhla - RBAC Permission Classes
INSTRUCTIONS.md: "Always enforce Role-Based Access Control (RBAC) in Django APIs"
REQUIREMENTS.md ke mutabiq har role ke specific privileges defined hain.
"""

from rest_framework.permissions import BasePermission
from accounts.models import User


class IsNotBanned(BasePermission):
    """
    Banned users ko API access deny karo.
    REQUIREMENTS.md: 3-Strike Rule — banned users kuch bhi nahi kar sakte.
    """
    message = 'Tumhara account banned hai. Ban period khatam hone tak wait karo.'

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return not request.user.is_banned


class IsCitizen(BasePermission):
    """Basic authenticated citizen — sabse kam permission level."""
    message = 'Sirf registered citizens ye action kar sakte hain.'

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_active
            and not request.user.is_banned
        )


class IsMinister(BasePermission):
    """
    Kisi bhi level ka Minister — Mohalla, City, ya Supreme.
    REQUIREMENTS.md: Ministers ke special privileges hain.
    """
    message = 'Ye action sirf Ministers ke liye hai.'

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.is_minister and not request.user.is_banned


class IsMohallaMinister(BasePermission):
    """
    Mohalla Minister ya usse upar ka role.
    REQUIREMENTS.md: Mohalla Minister forms cabinet of max 5 members.
    """
    message = 'Ye action sirf Mohalla Minister ya usse upar ke roles ke liye hai.'

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role in (
            User.Role.MOHALLA_MINISTER,
            User.Role.CITY_MINISTER,
            User.Role.SUPREME_MINISTER,
        ) and not request.user.is_banned


class IsCityMinister(BasePermission):
    """
    City Minister ya Supreme Minister.
    REQUIREMENTS.md: City Cabinet 11 roles — Home Minister, I&B, Law, etc.
    """
    message = 'Ye action sirf City Minister ya Supreme Minister ke liye hai.'

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role in (
            User.Role.CITY_MINISTER,
            User.Role.SUPREME_MINISTER,
        ) and not request.user.is_banned


class IsSupremeMinister(BasePermission):
    """
    Supreme Minister — God-mode access.
    REQUIREMENTS.md: "God-mode view across all Mohallas (Post, Comment, Like anywhere),
    issue direct Orders to any Mohalla, and flag/shadow-ban users for admin review."
    """
    message = 'Ye action sirf Supreme Minister ke liye hai.'

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return (
            request.user.role == User.Role.SUPREME_MINISTER
            and not request.user.is_banned
        )


class IsAdminOrSupremeMinister(BasePermission):
    """
    Django Admin ya Supreme Minister.
    High-level actions — announcements, ads, user banning, etc.
    """
    message = 'Ye action sirf Admin ya Supreme Minister ke liye hai.'

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return (
            request.user.is_staff
            or request.user.role == User.Role.SUPREME_MINISTER
        ) and not request.user.is_banned


class IsSameMohallaOrMinister(BasePermission):
    """
    Same mohalla ka user ya Minister.
    REQUIREMENTS.md: Cross-Mohalla users can view and Like/Dislike,
    but posting sirf own mohalla mein.
    """
    message = 'Tum sirf apne mohalla mein post kar sakte ho, ya Minister role chahiye.'

    def has_object_permission(self, request, view, obj):
        user = request.user
        # Supreme Minister sab jagah post kar sakta hai
        if user.role == User.Role.SUPREME_MINISTER:
            return True
        # Own mohalla check
        if hasattr(obj, 'mohalla'):
            return user.mohalla == obj.mohalla
        if hasattr(obj, 'mohalla_id'):
            return user.mohalla_id == obj.mohalla_id
        return False
