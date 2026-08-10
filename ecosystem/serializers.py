"""
Republic of Kandhla - Ecosystem Serializers
City, Mohalla, MohallaChangeRequest, Cabinet ke DRF serializers.
"""

from rest_framework import serializers
from ecosystem.models import City, Mohalla, MohallaChangeRequest, Cabinet
from accounts.serializers import UserMinimalSerializer


class CitySerializer(serializers.ModelSerializer):
    """City serializer — basic city info + mohalla count."""
    mohalla_count = serializers.IntegerField(source='mohallas.count', read_only=True)

    class Meta:
        model = City
        fields = [
            'id',
            'name',
            'state',
            'is_code_of_conduct_active',
            'mohalla_count',
        ]
        read_only_fields = fields


class CityDetailSerializer(serializers.ModelSerializer):
    """
    City detail serializer — Samvidhan content bhi include hota hai.
    SCHEMA.md: GET /api/system/samvidhan/{city_id}/
    """
    mohallas = serializers.SerializerMethodField()

    class Meta:
        model = City
        fields = [
            'id',
            'name',
            'state',
            'samvidhan_content',
            'is_code_of_conduct_active',
            'mohallas',
        ]
        read_only_fields = fields

    def get_mohallas(self, obj):
        """City ke saare mohallas return karo."""
        return MohallaSerializer(obj.mohallas.all(), many=True).data


class MohallaSerializer(serializers.ModelSerializer):
    """Mohalla serializer — city ke andar micro-constituency."""
    city_name = serializers.CharField(source='city.name', read_only=True)

    class Meta:
        model = Mohalla
        fields = [
            'id',
            'city',
            'city_name',
            'name',
            'population_count',
        ]
        read_only_fields = fields


class MohallaChangeRequestCreateSerializer(serializers.ModelSerializer):
    """
    Mohalla Change Request submit karo.
    REQUIREMENTS.md: "To change, they must submit a Mohalla Change Request
    which the Django Admin must approve."
    """

    class Meta:
        model = MohallaChangeRequest
        fields = ['target_mohalla', 'reason']

    def validate_target_mohalla(self, value):
        """Same mohalla mein request nahi de sakte."""
        user = self.context['request'].user
        if user.mohalla and user.mohalla.id == value.id:
            raise serializers.ValidationError(
                'Tum pehle se isi mohalla mein ho. Alag mohalla select karo.'
            )
        return value

    def validate(self, data):
        """
        REQUIREMENTS.md: "All requests freeze automatically when an election date is announced."
        Election active hone par request submit nahi ho sakti.
        """
        user = self.context['request'].user
        # Check if any active election exists in user's city
        from election.models import Election
        active_election = Election.objects.filter(
            city=user.city,
        ).exclude(
            phase=Election.Phase.COMPLETED,
        ).exists()

        if active_election:
            raise serializers.ValidationError(
                'Election chal rahi hai — Mohalla Change Requests abhi freeze hain.'
            )

        # Check for existing pending request
        pending_exists = MohallaChangeRequest.objects.filter(
            user=user,
            status=MohallaChangeRequest.Status.PENDING,
        ).exists()

        if pending_exists:
            raise serializers.ValidationError(
                'Tumhari ek pending request pehle se hai. Pehle uska result aane do.'
            )

        return data

    def create(self, validated_data):
        """Request create karte waqt user auto-set hoga."""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class MohallaChangeRequestSerializer(serializers.ModelSerializer):
    """Mohalla Change Request read serializer — status tracking."""
    user_name = serializers.CharField(source='user.name', read_only=True)
    target_mohalla_name = serializers.CharField(source='target_mohalla.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = MohallaChangeRequest
        fields = [
            'id',
            'user',
            'user_name',
            'target_mohalla',
            'target_mohalla_name',
            'reason',
            'status',
            'status_display',
            'created_at',
        ]
        read_only_fields = fields


class CabinetSerializer(serializers.ModelSerializer):
    """
    Cabinet member serializer — VIP badge info ke saath.
    REQUIREMENTS.md: City Cabinet (max 11), Mohalla Cabinet (max 5).
    """
    user_details = UserMinimalSerializer(source='user', read_only=True)
    city_name = serializers.CharField(source='city.name', read_only=True, default=None)
    mohalla_name = serializers.CharField(source='mohalla.name', read_only=True, default=None)

    class Meta:
        model = Cabinet
        fields = [
            'id',
            'user',
            'user_details',
            'city',
            'city_name',
            'mohalla',
            'mohalla_name',
            'department_name',
            'ruby_color',
            'is_active',
        ]
        read_only_fields = fields


class SamvidhanSerializer(serializers.ModelSerializer):
    """
    Samvidhan (Constitution) serializer.
    SCHEMA.md: GET /api/system/samvidhan/{city_id}/
    Sirf samvidhan HTML content return karta hai.
    """

    class Meta:
        model = City
        fields = ['id', 'name', 'samvidhan_content']
        read_only_fields = fields


class EngineeredBySerializer(serializers.Serializer):
    """
    Engineered By screen ka serializer.
    SCHEMA.md: GET /api/team/engineered-by/
    Dynamic JSON array of core development team members.
    """
    name = serializers.CharField()
    role = serializers.CharField()
    avatar_url = serializers.URLField(required=False, default='')
    github_url = serializers.URLField(required=False, default='')
