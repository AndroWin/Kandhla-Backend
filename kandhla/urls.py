"""
Republic of Kandhla - URL Configuration
Root URL conf jo saare app-level URLs ko include karta hai.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def api_root(request):
    return JsonResponse({
        "message": "Welcome to Republic of Kandhla API",
        "status": "Online",
        "version": "1.0"
    })

urlpatterns = [
    # API Root
    path('', api_root, name='api-root'),
    
    # Django Admin Panel
    path('admin/', admin.site.urls),

    # Custom Ecosystem Dashboard
    path('dashboard/', include('master_control.urls')),

    # API Endpoints - App wise routing
    path('api/auth/', include('accounts.urls')),
    path('api/', include('ecosystem.urls')),
    path('api/', include('content.urls')),
    path('api/', include('election.urls')),
]

# Development mein media files serve karne ke liye
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
