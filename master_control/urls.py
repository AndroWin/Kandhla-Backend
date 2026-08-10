from django.urls import path
from .views import (
    MasterDashboardView, UsersView, ContentView, 
    AdsView, ElectionsView, DashboardStatsAPI, CityManagementAPI,
    UserManagementAPI, ContentManagementAPI, AdsManagementAPI, ElectionsAPI
)

app_name = 'master_control'

urlpatterns = [
    # Separate Dashboard Pages
    path('', MasterDashboardView.as_view(), name='index'),
    path('users/', UsersView.as_view(), name='users'),
    path('content/', ContentView.as_view(), name='content'),
    path('ads/', AdsView.as_view(), name='ads'),
    path('elections/', ElectionsView.as_view(), name='elections'),

    # APIs for SPA
    path('api/stats/', DashboardStatsAPI.as_view(), name='api-stats'),
    path('api/cities/', CityManagementAPI.as_view(), name='api-cities'),
    path('api/users/', UserManagementAPI.as_view(), name='api-users'),
    path('api/content/', ContentManagementAPI.as_view(), name='api-content'),
    path('api/ads/', AdsManagementAPI.as_view(), name='api-ads'),
    path('api/elections/', ElectionsAPI.as_view(), name='api-elections'),
]
