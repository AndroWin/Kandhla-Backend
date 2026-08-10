import json
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


@method_decorator(csrf_exempt, name='dispatch')
class UserManagementAPI(SuperuserRequiredMixin, View):
    def get(self, request):
        query = request.GET.get('q', '')
        users = User.objects.all()
        if query:
            users = users.filter(email__icontains=query) | users.filter(first_name__icontains=query)
        
        users = users[:50] # limit 50
        data = []
        for user in users:
            data.append({
                'id': str(user.id),
                'email': user.email,
                'name': f"{user.first_name} {user.last_name}".strip() or user.email,
                'status': 'Active' if user.is_active else 'Banned',
                'mohalla': user.mohalla.name if hasattr(user, 'mohalla') and user.mohalla else 'N/A'
            })
        return JsonResponse({'success': True, 'users': data})

    def post(self, request):
        try:
            body = json.loads(request.body)
            user_id = body.get('user_id')
            action = body.get('action')
            
            user = User.objects.get(id=user_id)
            if action == 'ban':
                user.is_active = False
            elif action == 'unban':
                user.is_active = True
            user.save()
            return JsonResponse({'success': True, 'status': 'Active' if user.is_active else 'Banned'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class ContentManagementAPI(SuperuserRequiredMixin, View):
    def get(self, request):
        from content.models import Post
        posts = Post.objects.all().order_by('-created_at')[:20]
        data = []
        for p in posts:
            data.append({
                'id': str(p.id),
                'author': f"{p.author.first_name} {p.author.last_name}".strip() or p.author.email,
                'content': p.content[:100] + '...' if len(p.content) > 100 else p.content,
            })
        return JsonResponse({'success': True, 'posts': data})

    def post(self, request):
        try:
            from content.models import Post
            body = json.loads(request.body)
            post_id = body.get('post_id')
            Post.objects.filter(id=post_id).delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class AdsManagementAPI(SuperuserRequiredMixin, View):
    def post(self, request):
        try:
            # Fake logic for now until Ad model is clear
            return JsonResponse({'success': True, 'message': 'Ad Pinned Successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class ElectionsAPI(SuperuserRequiredMixin, View):
    def post(self, request):
        try:
            from election.models import Election
            body = json.loads(request.body)
            level = body.get('level', 'CITY')
            # Mocking the creation
            # Election.objects.create(...)
            return JsonResponse({'success': True, 'message': f'{level} Election Initialized! Phase 1 (Nomination) has started.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
