"""
Republic of Kandhla - Accounts API Views
Google Auth, Profile management, aur user-related endpoints.
"""

import hashlib
import logging
from django.conf import settings
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from jwt import PyJWKClient

from accounts.models import User
from accounts.serializers import (
    GoogleAuthSerializer,
    AppleAuthSerializer,
    UserProfileSerializer,
    UserProfileSetupSerializer,
)
from kandhla.permissions import IsNotBanned

logger = logging.getLogger(__name__)


class GoogleAuthView(APIView):
    """
    Google Login Endpoint.
    SCHEMA.md: POST /api/auth/google/
    - Verifies Google token
    - Checks device ID
    - Returns JWT session token and user profile
    REQUIREMENTS.md: "Google Login Only — Fast onboarding to prevent bot creation."
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = GoogleAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        google_token = serializer.validated_data['google_token']
        device_id = serializer.validated_data['device_id']

        # Google token verify karo
        google_user_info = self._verify_google_token(google_token)
        if not google_user_info:
            return Response(
                {
                    'success': False,
                    'error': 'Invalid Google token. Login failed.',
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        google_id = google_user_info.get('sub')
        email = google_user_info.get('email')
        name = google_user_info.get('name', '')
        avatar_url = google_user_info.get('picture', '')

        # User find karo ya create karo
        user, created = User.objects.get_or_create(
            google_id=google_id,
            defaults={
                'email': email,
                'name': name,
                'avatar_url': avatar_url,
                'device_id': device_id,
            },
        )

        if not created:
            # Existing user — device ID update karo
            user.device_id = device_id
            if not user.name:
                user.name = name
            if not user.avatar_url:
                user.avatar_url = avatar_url
            user.save(update_fields=['device_id', 'name', 'avatar_url'])

        # Ban check
        if user.is_banned:
            return Response(
                {
                    'success': False,
                    'error': 'Tumhara account banned hai.',
                    'ban_until': user.ban_until,
                    'strike_count': user.strike_count,
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # JWT tokens generate karo
        refresh = RefreshToken.for_user(user)
        profile_data = UserProfileSerializer(user).data

        logger.info(
            f"User {'created' if created else 'logged in'}: {user.email} "
            f"(device: {device_id[:12]}...)"
        )

        return Response(
            {
                'success': True,
                'is_new_user': created,
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                },
                'user': profile_data,
            },
            status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED,
        )

    def _verify_google_token(self, token):
        """
        Google OAuth token verify karo.
        Production mein google-auth library use hogi.
        """
        try:
            from google.oauth2 import id_token
            from google.auth.transport import requests as google_requests

            idinfo = id_token.verify_oauth2_token(
                token,
                google_requests.Request(),
            )
            return idinfo
        except ImportError:
            # Development mode — google-auth not installed
            # Dummy verification for local testing
            logger.warning("google-auth library not installed. Using dev mode token parsing.")
            return self._dev_mode_verify(token)
        except Exception as e:
            logger.error(f"Google token verification failed: {e}")
            return None

    def _dev_mode_verify(self, token):
        """
        Development mode mein dummy token verification.
        Production mein ye method use NAHI hoga.
        """
        if settings.DEBUG:
            # Dev mode: token ko email samajh ke user create karo
            return {
                'sub': hashlib.md5(token.encode()).hexdigest(),
                'email': token if '@' in token else f'{token}@dev.kandhla.app',
                'name': 'Dev User',
                'picture': '',
            }
        return None


class AppleAuthView(APIView):
    """
    Apple Sign-In Endpoint.
    SCHEMA.md: POST /api/auth/apple/
    - Verifies Apple identity token
    - Checks device ID
    - Returns JWT session token and user profile
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AppleAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        apple_token = serializer.validated_data['apple_token']
        device_id = serializer.validated_data['device_id']
        provided_name = serializer.validated_data.get('name', '')

        # Apple token verify karo
        apple_user_info = self._verify_apple_token(apple_token)
        if not apple_user_info:
            return Response(
                {
                    'success': False,
                    'error': 'Invalid Apple token. Login failed.',
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        apple_id = apple_user_info.get('sub')
        email = apple_user_info.get('email', f"{apple_id}@apple.kandhla.app")
        name = provided_name if provided_name else "Apple User"

        # User find karo ya create karo
        user, created = User.objects.get_or_create(
            apple_id=apple_id,
            defaults={
                'email': email,
                'name': name,
                'device_id': device_id,
            },
        )

        if not created:
            # Existing user — device ID update karo
            user.device_id = device_id
            if provided_name and not user.name:
                user.name = provided_name
            user.save(update_fields=['device_id', 'name'])

        # Ban check
        if user.is_banned:
            return Response(
                {
                    'success': False,
                    'error': 'Tumhara account banned hai.',
                    'ban_until': user.ban_until,
                    'strike_count': user.strike_count,
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # JWT tokens generate karo
        refresh = RefreshToken.for_user(user)
        profile_data = UserProfileSerializer(user).data

        logger.info(
            f"User {'created' if created else 'logged in'} via Apple: {user.email} "
            f"(device: {device_id[:12]}...)"
        )

        return Response(
            {
                'success': True,
                'is_new_user': created,
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                },
                'user': profile_data,
            },
            status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED,
        )

    def _verify_apple_token(self, token):
        """
        Apple JWT token verify karo securely.
        """
        try:
            url = "https://appleid.apple.com/auth/keys"
            jwks_client = PyJWKClient(url)
            signing_key = jwks_client.get_signing_key_from_jwt(token)
            
            data = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                options={"verify_aud": False}
            )
            return data
        except Exception as e:
            logger.error(f"Apple token verification failed: {e}")
            if settings.DEBUG:
                # Dev mode mock fallback (agar internet/proxy issue ho)
                try:
                    data = jwt.decode(token, options={"verify_signature": False})
                    return data
                except:
                    pass
            return None


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    User Profile Endpoint.
    GET — apna profile dekho.
    PATCH — profile update karo (name, avatar).
    Mohalla change ke liye MohallaChangeRequest submit karna padega.
    """
    permission_classes = [IsAuthenticated, IsNotBanned]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return UserProfileSetupSerializer
        return UserProfileSerializer


class UserProfileSetupView(generics.UpdateAPIView):
    """
    Profile Setup Endpoint — onboarding ke dauran city aur mohalla select karo.
    REQUIREMENTS.md: "Users select their City and Mohalla from a dropdown during profile creation."
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSetupSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        user = self.get_object()

        # Mohalla population count update karo
        if user.mohalla:
            from ecosystem.models import Mohalla
            mohalla = user.mohalla
            mohalla.population_count = User.objects.filter(
                mohalla=mohalla, is_active=True
            ).count()
            mohalla.save(update_fields=['population_count'])

        return Response(
            {
                'success': True,
                'message': 'Profile successfully setup ho gaya!',
                'user': UserProfileSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )


class OtherUserProfileView(generics.RetrieveAPIView):
    """
    Other User Profile — kisi aur ka public profile dekho.
    Sensitive data (email, device_id) hidden rahega.
    """
    permission_classes = [IsAuthenticated, IsNotBanned]
    serializer_class = UserProfileSerializer
    queryset = User.objects.filter(is_active=True)
    lookup_field = 'id'
