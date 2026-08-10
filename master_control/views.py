import json
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from accounts.models import User
from ecosystem.models import City, Mohalla
from content.models import Post

class MockAuthMixin:
    """
    Bypass session authentication for the Flutter Web Admin (Local Dev).
    In production, this would use JWT TokenAuthentication.
    """
    def dispatch(self, request, *args, **kwargs):
        # Allow all cross-origin or local requests for this phase
        return super().dispatch(request, *args, **kwargs)


@method_decorator(csrf_exempt, name='dispatch')
class DashboardStatsAPI(MockAuthMixin, View):
    """API for the Super Dashboard (1.1)."""
    def get(self, request):
        return JsonResponse({
            'success': True,
            'cities': City.objects.count(),
            'users': User.objects.count(),
            'server_health': 'Optimal'
        })


@method_decorator(csrf_exempt, name='dispatch')
class CityManagementAPI(MockAuthMixin, View):
    """API for City CRUD."""
    def get(self, request):
        cities = City.objects.all().prefetch_related('mohallas')
        data = []
        for city in cities:
            data.append({
                'id': str(city.id),
                'name': city.name,
                'mohalla_count': city.mohallas.count(),
                'emergency_rule': city.is_emergency_rule_active,
                'achaar_sanhita': city.is_code_of_conduct_active,
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
class UserManagementAPI(MockAuthMixin, View):
    def get(self, request):
        query = request.GET.get('q', '')
        users = User.objects.all()
        if query:
            users = users.filter(email__icontains=query) | users.filter(name__icontains=query)
        
        users = users[:50]
        data = []
        for user in users:
            data.append({
                'id': str(user.id),
                'email': user.email,
                'name': user.name or user.email,
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
class ContentManagementAPI(MockAuthMixin, View):
    def get(self, request):
        posts = Post.objects.all().order_by('-created_at')[:20]
        data = []
        for p in posts:
            data.append({
                'id': str(p.id),
                'author': p.user.name or p.user.email,
                'content': p.content_text[:100] + '...' if p.content_text and len(p.content_text) > 100 else p.content_text,
                'type': p.post_type,
            })
        return JsonResponse({'success': True, 'posts': data})

    def post(self, request):
        try:
            body = json.loads(request.body)
            
            # If toggle emergency rule
            if 'emergency_rule' in body:
                city = City.objects.first() # Assume single city for prototype
                if city:
                    city.is_emergency_rule_active = body['emergency_rule']
                    city.save()
                    return JsonResponse({'success': True, 'message': 'Emergency Rule updated'})

            # If delete post
            post_id = body.get('post_id')
            if post_id:
                Post.objects.filter(id=post_id).delete()
                return JsonResponse({'success': True, 'message': 'Post deleted'})
            
            return JsonResponse({'success': False, 'error': 'Invalid action'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class AdsManagementAPI(MockAuthMixin, View):
    def post(self, request):
        try:
            body = json.loads(request.body)
            title = body.get('title', 'Local Ad')
            phone = body.get('phone', '')
            
            # Create a Post of type AD so it shows up in the User App Feed
            # We need an admin user and a mohalla
            admin_user = User.objects.filter(is_superuser=True).first()
            mohalla = Mohalla.objects.first()
            
            if not admin_user or not mohalla:
                return JsonResponse({'success': False, 'error': 'System lacks admin or mohalla to push ad'}, status=400)

            content = f"📣 {title}\nContact: {phone}"
            Post.objects.create(
                user=admin_user,
                mohalla=mohalla,
                content_text=content,
                post_type=Post.PostType.AD,
            )

            return JsonResponse({'success': True, 'message': 'Ad pushed to feed'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class ElectionsAPI(MockAuthMixin, View):
    def post(self, request):
        try:
            body = json.loads(request.body)
            level = body.get('level', 'CITY')
            
            if 'achaar_sanhita' in body:
                city = City.objects.first()
                if city:
                    city.is_code_of_conduct_active = body['achaar_sanhita']
                    city.save()
                    return JsonResponse({'success': True, 'message': 'Achaar Sanhita updated'})

            return JsonResponse({'success': True, 'message': f'{level} Election Initialized! Phase 1 has started.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
