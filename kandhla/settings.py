"""
Republic of Kandhla - Django Settings
Production-ready configuration for the hyper-local virtual political ecosystem.
Tech Stack: Django + DRF + PostgreSQL + Celery + Redis + Firebase
"""

import os
from pathlib import Path
from datetime import timedelta
import dj_database_url

# ============================================================
# BASE DIRECTORY
# ============================================================
BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================================
# SECURITY (Override in production via environment variables)
# ============================================================
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'dev-insecure-key-republic-of-kandhla-change-in-production'
)

DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() in ('true', '1', 'yes')

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Automatically add Render's external hostname if deployed there
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# ============================================================
# APPLICATION DEFINITION
# ============================================================
INSTALLED_APPS = [
    'jazzmin',  # Must be first
    # Django core apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'corsheaders',
    'django_filters',
    'django_celery_beat',

    # Project apps - Republic of Kandhla
    'accounts.apps.AccountsConfig',
    'ecosystem.apps.EcosystemConfig',
    'content.apps.ContentConfig',
    'election.apps.ElectionConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Republic of Kandhla - Custom Middleware
    'kandhla.middleware.RequestLoggingMiddleware',
    'kandhla.middleware.BanCheckMiddleware',
    'kandhla.middleware.AchaarSanhitaMiddleware',
    'kandhla.middleware.GlobalExceptionMiddleware',
]

ROOT_URLCONF = 'kandhla.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ============================================================
# JAZZMIN ADMIN UI SETTINGS
# ============================================================
JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "Republic of Kandhla Admin",

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "Kandhla Backend",

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "Kandhla Admin",

    # Welcome text on the login screen
    "welcome_sign": "Welcome to the Supreme Minister Dashboard",

    # Copyright on the footer
    "copyright": "Republic of Kandhla Ltd",

    # The model admin to search from the search bar, search bar omitted if excluded
    "search_model": ["accounts.User"],

    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": "avatar_url",

    # Whether to display the side menu
    "show_sidebar": True,

    # Whether to aut expand the menu
    "navigation_expanded": True,

    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.1.0,5.1.1,5.1.2,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "auth": "fas fa-users-cog",
        "accounts.user": "fas fa-user",
        "ecosystem.city": "fas fa-city",
        "ecosystem.mohalla": "fas fa-map-marker-alt",
        "content.post": "fas fa-file-alt",
        "election.election": "fas fa-vote-yea",
    },
    
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    
    "related_modal_active": False,
    "custom_css": None,
    "custom_js": None,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {"accounts.user": "collapsible", "auth.group": "vertical_tabs"},
    
    # Hide confusing technical apps for non-tech users
    "hide_apps": ["django_celery_beat", "auth"],
    "hide_models": ["auth.Group", "auth.User"],
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-primary",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "lumen",
    "dark_mode_theme": "darkly",
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-outline-info",
        "warning": "btn-outline-warning",
        "danger": "btn-outline-danger",
        "success": "btn-outline-success"
    }
}

WSGI_APPLICATION = 'kandhla.wsgi.application'

# ============================================================
# DATABASE - PostgreSQL (SCHEMA.md ke mutabiq)
# ============================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Override with Supabase/Cloud PostgreSQL if DATABASE_URL is provided in environment variables
if 'DATABASE_URL' in os.environ:
    DATABASES['default'] = dj_database_url.config(
        conn_max_age=600,
        conn_health_checks=True,
        ssl_require=True
    )

# ============================================================
# CUSTOM USER MODEL (accounts app mein defined hai)
# ============================================================
AUTH_USER_MODEL = 'accounts.User'

# ============================================================
# PASSWORD VALIDATION
# ============================================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ============================================================
# INTERNATIONALIZATION
# ============================================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# ============================================================
# STATIC & MEDIA FILES
# ============================================================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ============================================================
# DEFAULT PRIMARY KEY TYPE - UUID (SCHEMA.md ke mutabiq)
# ============================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================================
# DJANGO REST FRAMEWORK CONFIGURATION
# ============================================================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '30/minute',
        'user': '120/minute',
    },
    'EXCEPTION_HANDLER': 'kandhla.utils.custom_exception_handler',
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}

# ============================================================
# SIMPLE JWT - Token Configuration
# ============================================================
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=6),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# ============================================================
# CELERY + REDIS (Election phase shifts, Achaar Sanhita automation)
# ============================================================
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/1')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# Celery Beat — Periodic Tasks Schedule
CELERY_BEAT_SCHEDULE = {
    # Ban expiry check — har 15 minute
    'check-ban-expiry': {
        'task': 'accounts.tasks.check_ban_expiry',
        'schedule': timedelta(minutes=15),
    },
    # Vote queue processing — har 2 minute
    'process-vote-queue': {
        'task': 'election.tasks.process_vote_queue',
        'schedule': timedelta(minutes=2),
    },
    # Concern auto-escalation — har 30 minute
    'auto-escalate-concerns': {
        'task': 'content.tasks.auto_escalate_concerns',
        'schedule': timedelta(minutes=30),
    },
    # Mohalla population sync — daily raat 2 baje
    'update-mohalla-populations': {
        'task': 'accounts.tasks.update_mohalla_populations',
        'schedule': timedelta(hours=24),
    },
    # Election scheduling check — daily subah 6 baje
    'schedule-next-elections': {
        'task': 'election.tasks.schedule_next_elections',
        'schedule': timedelta(hours=24),
    },
    # Old posts cleanup — weekly
    'cleanup-old-posts': {
        'task': 'content.tasks.cleanup_old_posts',
        'schedule': timedelta(days=7),
    },
    # Firebase interaction sync — har 5 minute
    'sync-interaction-counts': {
        'task': 'content.tasks.sync_interaction_counts',
        'schedule': timedelta(minutes=5),
    },
}

# ============================================================
# CORS CONFIGURATION
# ============================================================
CORS_ALLOW_ALL_ORIGINS = DEBUG  # Production mein specific origins set karna
CORS_ALLOWED_ORIGINS = os.environ.get(
    'CORS_ALLOWED_ORIGINS', 'http://localhost:3000'
).split(',')

# ============================================================
# FIREBASE CONFIGURATION (FCM + Realtime DB sync)
# ============================================================
FIREBASE_CREDENTIALS_PATH = os.environ.get(
    'FIREBASE_CREDENTIALS_PATH',
    BASE_DIR / 'firebase-credentials.json'
)

# ============================================================
# REPUBLIC OF KANDHLA - CUSTOM APP SETTINGS
# ============================================================
KANDHLA_SETTINGS = {
    # Credibility Score thresholds
    'MIN_CREDIBILITY_FOR_NOMINATION': 500,
    'CREDIBILITY_BOOST_PER_SUPPORT': 5,
    'CREDIBILITY_PENALTY_PER_STRIKE': 50,

    # Election configuration
    'MAX_CITY_CABINET_SIZE': 11,
    'MAX_MOHALLA_CABINET_SIZE': 5,
    'CITY_ELECTION_CYCLE_DAYS': 90,       # Har 3 mahine
    'MOHALLA_ELECTION_CYCLE_DAYS': 30,    # Har 1 mahina

    # Moderation - 3-Strike Rule
    'STRIKE_1_BAN_HOURS': 6,
    'STRIKE_2_BAN_HOURS': 24,
    'STRIKE_3_BAN_HOURS': 72,
    'STRIKE_4_PERMANENT_BAN': True,

    # Voting security
    'ONE_DEVICE_ONE_VOTE': True,
    'VOTE_QUEUE_REDIS_KEY': 'kandhla:vote_queue',

    # Top candidates for symbol allocation
    'MAX_CITY_CANDIDATES': 30,
}

# ============================================================
# LOGGING CONFIGURATION (Global exception handling)
# ============================================================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} {name} {module}.{funcName}:{lineno} - {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'kandhla.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'WARNING',
            'propagate': False,
        },
        'accounts': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'ecosystem': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'content': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'election': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
