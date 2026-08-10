"""
Republic of Kandhla - Ecosystem URL Configuration
City, Mohalla, Cabinet, Samvidhan, Engineered By endpoints.
"""

from django.urls import path
from ecosystem.views import (
    CityListView,
    CityDetailView,
    MohallaListView,
    MohallaChangeRequestCreateView,
    MohallaChangeRequestListView,
    CabinetListView,
    SamvidhanView,
    EngineeredByView,
)

app_name = 'ecosystem'

urlpatterns = [
    # City & Mohalla — Onboarding dropdowns
    path('cities/', CityListView.as_view(), name='city-list'),
    path('cities/<uuid:id>/', CityDetailView.as_view(), name='city-detail'),
    path('cities/<uuid:city_id>/mohallas/', MohallaListView.as_view(), name='mohalla-list'),

    # Mohalla Change Request
    path('mohalla/change-request/', MohallaChangeRequestCreateView.as_view(), name='mohalla-change-create'),
    path('mohalla/change-requests/', MohallaChangeRequestListView.as_view(), name='mohalla-change-list'),

    # Cabinet
    path('cabinet/', CabinetListView.as_view(), name='cabinet-list'),

    # Samvidhan (Constitution)
    path('system/samvidhan/<uuid:city_id>/', SamvidhanView.as_view(), name='samvidhan'),

    # Engineered By (Dev Team)
    path('team/engineered-by/', EngineeredByView.as_view(), name='engineered-by'),
]
