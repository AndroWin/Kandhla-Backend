from django.urls import path
from .views import MasterDashboardView, DashboardStatsAPI, CityManagementAPI

app_name = 'master_control'

urlpatterns = [
    # SPA HTML Entry Point
    path('', MasterDashboardView.as_view(), name='index'),

    # APIs for SPA
    path('api/stats/', DashboardStatsAPI.as_view(), name='api-stats'),
    path('api/cities/', CityManagementAPI.as_view(), name='api-cities'),
]
