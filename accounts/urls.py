"""
Republic of Kandhla - Accounts URL Configuration
Auth endpoints: Google login, JWT tokens, Profile management.
SCHEMA.md: POST /api/auth/google/ -> Verifies Google token, checks device ID, returns JWT + profile.
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.views import (
    GoogleAuthView,
    AppleAuthView,
    UserProfileView,
    UserProfileSetupView,
    OtherUserProfileView,
)

app_name = 'accounts'

urlpatterns = [
    # POST /api/auth/google/ -> Google token verify, Device ID check, JWT return
    path('google/', GoogleAuthView.as_view(), name='google-login'),
    # POST /api/auth/apple/ -> Apple token verify, Device ID check, JWT return
    path('apple/', AppleAuthView.as_view(), name='apple-login'),

    # POST /api/auth/token/refresh/ -> JWT refresh
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    # GET/PATCH /api/auth/profile/ -> Apna profile dekho/update karo
    path('profile/', UserProfileView.as_view(), name='my-profile'),

    # PATCH /api/auth/profile/setup/ -> Onboarding — City/Mohalla select
    path('profile/setup/', UserProfileSetupView.as_view(), name='profile-setup'),

    # GET /api/auth/user/{id}/ -> Kisi aur ka public profile
    path('user/<uuid:id>/', OtherUserProfileView.as_view(), name='other-profile'),
]
