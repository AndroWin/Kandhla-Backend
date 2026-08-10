"""
Republic of Kandhla - Custom Middleware
INSTRUCTIONS.md: "Implement global exception handlers in Django (middleware logging)
to prevent unexpected app crashes."

Middleware stack:
1. BanCheckMiddleware — Banned users ko har request pe block karo
2. RequestLoggingMiddleware — Saari API requests log karo
3. AchaarSanhitaMiddleware — Code of Conduct active hone par posting block karo
"""

import logging
import time
from django.http import JsonResponse
from django.utils import timezone

logger = logging.getLogger(__name__)


class BanCheckMiddleware:
    """
    Banned users ko har API request pe block karo.
    REQUIREMENTS.md: 3-Strike Rule enforcement — banned users kuch bhi nahi kar sakte.
    
    Ye middleware authentication ke baad chalta hai.
    Banned user ko 403 Forbidden response milta hai.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Admin panel aur auth endpoints ko bypass karo
        if request.path.startswith('/admin/') or request.path.startswith('/api/auth/'):
            return self.get_response(request)

        # Authenticated user ka ban status check karo
        if hasattr(request, 'user') and request.user.is_authenticated:
            user = request.user

            # Permanent ban check (strike >= 4)
            if user.strike_count >= 4:
                return JsonResponse(
                    {
                        'success': False,
                        'error': 'Tumhara account permanently banned hai.',
                        'strike_count': user.strike_count,
                        'is_permanent': True,
                    },
                    status=403,
                )

            # Timed ban check
            if user.ban_until and user.ban_until > timezone.now():
                remaining = user.ban_until - timezone.now()
                hours_remaining = remaining.total_seconds() / 3600

                return JsonResponse(
                    {
                        'success': False,
                        'error': f'Tumhara account banned hai. '
                                 f'{hours_remaining:.1f} ghante baad ban khatam hoga.',
                        'ban_until': user.ban_until.isoformat(),
                        'strike_count': user.strike_count,
                        'is_permanent': False,
                    },
                    status=403,
                )

        return self.get_response(request)


class RequestLoggingMiddleware:
    """
    Saari API requests ka detailed logging.
    INSTRUCTIONS.md: Middleware logging for error prevention.
    
    Har request ka method, path, response status, aur execution time log hota hai.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        # Request info capture karo
        method = request.method
        path = request.path
        user = getattr(request, 'user', None)
        user_info = f" [{user.email}]" if user and hasattr(user, 'email') and user.is_authenticated else " [Anonymous]"

        response = self.get_response(request)

        # Execution time calculate karo
        duration = time.time() - start_time
        status_code = response.status_code

        # Static files aur admin assets skip karo
        if not path.startswith(('/static/', '/media/', '/favicon')):
            log_message = (
                f"{method} {path}{user_info} -> {status_code} "
                f"({duration:.3f}s)"
            )

            if status_code >= 500:
                logger.error(log_message)
            elif status_code >= 400:
                logger.warning(log_message)
            else:
                logger.info(log_message)

        return response


class AchaarSanhitaMiddleware:
    """
    Achaar Sanhita (Code of Conduct) enforcement middleware.
    REQUIREMENTS.md: "Code of Conduct applied automatically by Celery (Posting disabled)."
    
    Jab Achaar Sanhita active ho, toh POST requests for content creation block karo.
    Admin aur Supreme Minister exempt hain.
    """

    # Ye paths Achaar Sanhita ke dauran block honge
    BLOCKED_PATHS = [
        '/api/posts/create/',
        '/api/concerns/create/',
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Sirf POST requests check karo blocked paths pe
        if request.method == 'POST' and request.path in self.BLOCKED_PATHS:
            if hasattr(request, 'user') and request.user.is_authenticated:
                user = request.user

                # Admin aur Supreme Minister exempt hain
                if not user.is_staff:
                    from accounts.models import User
                    if user.role != User.Role.SUPREME_MINISTER:
                        # User ki city ka Achaar Sanhita status check karo
                        if user.city and user.city.is_code_of_conduct_active:
                            return JsonResponse(
                                {
                                    'success': False,
                                    'error': 'Achaar Sanhita (Code of Conduct) active hai. '
                                             'Election ke dauran posting disabled hai. '
                                             'Results ke baad feed unlock hoga.',
                                },
                                status=403,
                            )

        return self.get_response(request)


class GlobalExceptionMiddleware:
    """
    Global unhandled exception catch karo.
    INSTRUCTIONS.md: "Implement global exception handlers to prevent unexpected app crashes."
    
    DRF views ke liye utils.py mein custom_exception_handler hai,
    ye middleware non-DRF views ke liye safety net hai.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        """Unhandled exception ko catch karke clean error response do."""
        logger.exception(
            f"🔥 UNHANDLED EXCEPTION on {request.method} {request.path}: "
            f"{type(exception).__name__}: {exception}"
        )

        return JsonResponse(
            {
                'success': False,
                'error': {
                    'status_code': 500,
                    'detail': 'Server mein unexpected error aaya hai. '
                              'Humari team ko notify kar diya gaya hai.',
                },
            },
            status=500,
        )
