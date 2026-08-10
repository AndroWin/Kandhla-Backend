from django.urls import path
from .views import (
    DashboardStatsAPI, CityManagementAPI,
    UserManagementAPI, ContentManagementAPI, AdsManagementAPI, ElectionsAPI
)

app_name = 'master_control'

urlpatterns = [
    # APIs for Flutter Web Admin
    path('api/stats/', DashboardStatsAPI.as_view(), name='api-stats'),
    path('api/cities/', CityManagementAPI.as_view(), name='api-cities'),
    path('api/users/', UserManagementAPI.as_view(), name='api-users'),
    path('api/content/', ContentManagementAPI.as_view(), name='api-content'),
    path('api/ads/', AdsManagementAPI.as_view(), name='api-ads'),
    path('api/elections/', ElectionsAPI.as_view(), name='api-elections'),
]
