"""
Republic of Kandhla - Ecosystem API Views
City, Mohalla, Cabinet, Samvidhan, Engineered By endpoints.
"""

import logging
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from ecosystem.models import City, Mohalla, MohallaChangeRequest, Cabinet
from ecosystem.serializers import (
    CitySerializer,
    CityDetailSerializer,
    MohallaSerializer,
    MohallaChangeRequestCreateSerializer,
    MohallaChangeRequestSerializer,
    CabinetSerializer,
    SamvidhanSerializer,
    EngineeredBySerializer,
)
from kandhla.permissions import IsNotBanned

logger = logging.getLogger(__name__)


class CityListView(generics.ListAPIView):
    """
    All cities ki list — onboarding dropdown ke liye.
    """
    permission_classes = [AllowAny]
    serializer_class = CitySerializer
    queryset = City.objects.all()


class CityDetailView(generics.RetrieveAPIView):
    """
    City detail — mohallas ke saath.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CityDetailSerializer
    queryset = City.objects.all()
    lookup_field = 'id'


class MohallaListView(generics.ListAPIView):
    """
    City ke saare mohallas — onboarding dropdown aur explore ke liye.
    """
    permission_classes = [AllowAny]
    serializer_class = MohallaSerializer

    def get_queryset(self):
        city_id = self.kwargs.get('city_id')
        if city_id:
            return Mohalla.objects.filter(city_id=city_id)
        return Mohalla.objects.all()


class MohallaChangeRequestCreateView(generics.CreateAPIView):
    """
    Mohalla Change Request submit karo.
    REQUIREMENTS.md: "Users cannot change their Mohalla manually once set.
    To change, they must submit a Mohalla Change Request."
    Election ke dauran requests freeze ho jati hain.
    """
    permission_classes = [IsAuthenticated, IsNotBanned]
    serializer_class = MohallaChangeRequestCreateSerializer


class MohallaChangeRequestListView(generics.ListAPIView):
    """
    User ki apni Mohalla Change Requests ki list.
    """
    permission_classes = [IsAuthenticated, IsNotBanned]
    serializer_class = MohallaChangeRequestSerializer

    def get_queryset(self):
        return MohallaChangeRequest.objects.filter(user=self.request.user)


class CabinetListView(generics.ListAPIView):
    """
    City ya Mohalla ka active Cabinet dikhao.
    REQUIREMENTS.md: City Cabinet (max 11), Mohalla Cabinet (max 5).
    VIP badge info ke saath.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CabinetSerializer

    def get_queryset(self):
        queryset = Cabinet.objects.filter(is_active=True)
        city_id = self.request.query_params.get('city_id')
        mohalla_id = self.request.query_params.get('mohalla_id')

        if city_id:
            queryset = queryset.filter(city_id=city_id)
        if mohalla_id:
            queryset = queryset.filter(mohalla_id=mohalla_id)

        return queryset.select_related('user', 'city', 'mohalla')


class SamvidhanView(generics.RetrieveAPIView):
    """
    City ka Samvidhan (Constitution) return karo.
    SCHEMA.md: GET /api/system/samvidhan/{city_id}/
    HTML content return hota hai — Flutter WebView mein render hoga.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = SamvidhanSerializer
    queryset = City.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'city_id'


class EngineeredByView(APIView):
    """
    Dynamic dev team list.
    SCHEMA.md: GET /api/team/engineered-by/
    "Returns dynamic JSON array of core development team members
    for the 'Engineered By' screen."
    """
    permission_classes = [AllowAny]

    def get(self, request):
        # Dynamic team data — future mein database model se load hoga
        team_members = [
            {
                'name': 'Republic of Kandhla',
                'role': 'Lead Developer & Architect',
                'avatar_url': '',
                'github_url': '',
            },
        ]

        serializer = EngineeredBySerializer(team_members, many=True)
        return Response(
            {
                'success': True,
                'team': serializer.data,
            },
            status=status.HTTP_200_OK,
        )


from rest_framework.permissions import IsAdminUser
from django.contrib.auth import get_user_model
from content.models import Post

User = get_user_model()

class AdminDashboardStatsView(APIView):
    """
    Premium Admin Dashboard API - Returns stats for the Jazzmin custom UI.
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_users = User.objects.count()
        total_mohallas = Mohalla.objects.count()
        total_posts = Post.objects.count()
        total_revenue = "$12,500"  # Placeholder for premium feel
        
        # Fake chart data for the demo
        monthly_growth = [120, 200, 150, 400, 300, 500, 800, 1200, 1500, 1800, 2100, 2300]
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        return Response({
            "total_users": total_users,
            "total_mohallas": total_mohallas,
            "total_posts": total_posts,
            "total_revenue": total_revenue,
            "chart": {
                "labels": months,
                "data": monthly_growth
            }
        })
