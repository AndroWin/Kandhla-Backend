"""
Republic of Kandhla - Accounts Serializers
User registration, profile, Google auth ke liye DRF serializers.
"""

from rest_framework import serializers
from accounts.models import User


class GoogleAuthSerializer(serializers.Serializer):
    """
    Google Login Serializer.
    SCHEMA.md: POST /api/auth/google/
    Frontend se Google token aur device_id aayega,
    backend verify karega aur JWT + profile return karega.
    """
    google_token = serializers.CharField(
        required=True,
        help_text='Google OAuth ID token',
    )
    device_id = serializers.CharField(
        required=True,
        max_length=255,
        help_text='Physical device identifier for anti-fraud binding',
    )


class AppleAuthSerializer(serializers.Serializer):
    """
    Apple Sign-In Serializer.
    SCHEMA.md: POST /api/auth/apple/
    """
    apple_token = serializers.CharField(
        required=True,
        help_text='Apple Identity Token (JWT)',
    )
    device_id = serializers.CharField(
        required=True,
        max_length=255,
        help_text='Physical device identifier for anti-fraud binding',
    )
    name = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text='Full name provided by Apple (only on first login)',
    )


class UserProfileSerializer(serializers.ModelSerializer):
    """
    User Profile Serializer — public profile data.
    City aur Mohalla ka naam bhi include hota hai.
    """
    city_name = serializers.CharField(source='city.name', read_only=True, default=None)
    mohalla_name = serializers.CharField(source='mohalla.name', read_only=True, default=None)
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    is_banned = serializers.BooleanField(read_only=True)
    is_minister = serializers.BooleanField(read_only=True)
    can_nominate = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'name',
            'email',
            'avatar_url',
            'city',
            'city_name',
            'mohalla',
            'mohalla_name',
            'role',
            'role_display',
            'credibility_score',
            'strike_count',
            'is_banned',
            'is_minister',
            'can_nominate',
            'is_active',
            'created_at',
        ]
        read_only_fields = [
            'id',
            'email',
            'role',
            'credibility_score',
            'strike_count',
            'is_active',
            'created_at',
        ]


class UserProfileSetupSerializer(serializers.ModelSerializer):
    """
    Profile Setup Serializer — onboarding ke dauran city aur mohalla select karo.
    REQUIREMENTS.md: "Users select their City and Mohalla from a dropdown during profile creation."
    Mohalla ek baar set hone ke baad manually change nahi hoga.
    """

    class Meta:
        model = User
        fields = ['name', 'avatar_url', 'city', 'mohalla']

    def validate(self, data):
        """City aur Mohalla match honi chahiye."""
        city = data.get('city')
        mohalla = data.get('mohalla')
        if city and mohalla and mohalla.city_id != city.id:
            raise serializers.ValidationError({
                'mohalla': 'Ye mohalla selected city mein nahi hai.'
            })
        return data

    def update(self, instance, validated_data):
        """
        Profile update — agar mohalla pehle se set hai toh change nahi hoga.
        REQUIREMENTS.md: "Users cannot change their Mohalla manually once set."
        """
        if instance.mohalla and 'mohalla' in validated_data:
            if validated_data['mohalla'] != instance.mohalla:
                raise serializers.ValidationError({
                    'mohalla': 'Mohalla ek baar set hone ke baad change nahi ho sakta. Mohalla Change Request submit karo.'
                })
        return super().update(instance, validated_data)


class UserMinimalSerializer(serializers.ModelSerializer):
    """
    Minimal User Serializer — feed posts, candidates, etc. mein use hota hai.
    Sirf public display info.
    """
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'avatar_url', 'role', 'role_display', 'credibility_score']
        read_only_fields = fields
