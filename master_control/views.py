import json
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from accounts.models import User
from ecosystem.models import City, Mohalla


class SuperuserRequiredMixin(UserPassesTestMixin):
    """Ensure only superusers can access this dashboard."""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser


class MasterDashboardView(SuperuserRequiredMixin, TemplateView):
    template_name = 'master_control/index.html'

class UsersView(SuperuserRequiredMixin, TemplateView):
    template_name = 'master_control/users.html'

class ContentView(SuperuserRequiredMixin, TemplateView):
    template_name = 'master_control/content.html'

class AdsView(SuperuserRequiredMixin, TemplateView):
    template_name = 'master_control/ads.html'

class ElectionsView(SuperuserRequiredMixin, TemplateView):
    template_name = 'master_control/elections.html'


class DashboardStatsAPI(SuperuserRequiredMixin, View):
    """API for the Super Dashboard (1.1)."""
    def get(self, request):
        total_cities = City.objects.count()
        total_users = User.objects.count()
        
        return JsonResponse({
            'success': True,
            'cities': total_cities,
            'users': total_users,
            'server_health': 'Optimal'
        })


@method_decorator(csrf_exempt, name='dispatch')
class CityManagementAPI(SuperuserRequiredMixin, View):
    """API for City CRUD (1.2)."""
    def get(self, request):
        cities = City.objects.all().prefetch_related('mohallas')
        data = []
        for city in cities:
            data.append({
                'id': str(city.id),
                'name': city.name,
                'mohalla_count': city.mohallas.count()
            })
        return JsonResponse({'success': True, 'cities': data})

    def post(self, request):
        try:
            body = json.loads(request.body)
            name = body.get('name')
            state = body.get('state', 'Unknown')
            country = body.get('country', 'India')
            
            if name:
                City.objects.create(name=name, state=state, country=country)
                return JsonResponse({'success': True, 'message': 'City created'})
            return JsonResponse({'success': False, 'error': 'Name required'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
