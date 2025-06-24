"""
Django settings for optima project.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-40gl)s1=63_)n6(f&e9pf1w9yomxpg*-#c%&*wrjx%#@+34_ao'
DEBUG = True

ALLOWED_HOSTS = [
    'app.instafret.com', 'www.app.instafret.com', 'instafret.com', '.instafret.com',
    'web.eco-fret.com', '.eco-fret.com', 'localhost', '127.0.0.1'
]

# Application definition
INSTALLED_APPS = [
    'jazzmin',
    'optimasite.apps.OptimasiteConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    
    # New apps for shipment tracking
    'channels',
    'django_celery_beat',
    'django_celery_results',
]  # Fixed: Added missing closing bracket

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'optima.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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
]  # Fixed: Added missing closing bracket

WSGI_APPLICATION = 'optima.wsgi.application'
ASGI_APPLICATION = 'optima.asgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ecofgphh_optimafret',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        }
    }
}  # Fixed: Added missing closing bracket

# Redis Configuration
REDIS_URL = 'redis://localhost:6379/0'

# Django Channels Configuration
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [REDIS_URL],
        },
    },
}

# Celery Configuration
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Africa/Algiers'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Algiers'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Media files
MEDIA_URL = '/uploads/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'optimasite/uploads')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# CORS Configuration
CORS_ALLOWED_ORIGINS = [
    "https://eco-fret.com", "https://www.eco-fret.com", "https://web.eco-fret.com",
    "http://web.eco-fret.com", "http://197.240.168.85", "http://localhost:4200",
    "http://localhost:3000", "http://212.102.35.251", "http://197.240.91.76",
    "http://www.instafret.com", "https://www.instafret.com", "http://instafret.com",
    "https://instafret.com", "https://app.instafret.com", "http://app.instafret.com"
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = False

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'instafret.com'
EMAIL_USE_TLS = False
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'hello@instafret.com'
EMAIL_HOST_PASSWORD = 'J5OtSw3QW{G1'
DEFAULT_FROM_EMAIL = 'InstaFret <hello@instafret.com>'

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'optimasite': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
# Add this to your settings.py file

JAZZMIN_SETTINGS = {
    "site_title": "Optima Admin",
    "site_header": "Optima Freight Management",
    "site_brand": "Optima",
    "welcome_sign": "Welcome to Optima Admin Dashboard",
    "copyright": "Optima © 2025",
    "search_model": ["optimasite.users", "optimasite.companies", "optimasite.vehicles"],
    
    # Theme and styling
    "theme": "flatly",
    "dark_mode_theme": "darkly",
    
    # Top menu links
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Dashboard", "url": "/admin/", "permissions": ["auth.view_user"]},
        {"name": "API Docs", "url": "/api/", "new_window": True},
    ],
    
    # Model ordering and grouping
    "order_with_respect_to": [
        # Provider Theme
        "optimasite.companies",
        "optimasite.companytypes", 
        "optimasite.companyallservices",
        "optimasite.companyservices",
        
        # Clients Theme
        "optimasite.users",
        "optimasite.usertypes",
        "optimasite.usersaddresses",
        "optimasite.tokens",
        
        # Vehicles Theme  
        "optimasite.vehicles",
        "optimasite.vehiclecategories",
        "optimasite.vehiclesalloptions",
        "optimasite.vehiclesoptions",
        
        # Shipment Tracking Theme
        "optimasite.carriers",
        "optimasite.shipments",
        "optimasite.shipment_tags",
        "optimasite.shipment_followers",
        "optimasite.shipment_status_updates",
        "optimasite.broker_profiles",
        "optimasite.notification_logs",
        
        # Operations Theme
        "optimasite.requests",
        "optimasite.missions",
        "optimasite.attributions",
        "optimasite.requestoffers",
        "optimasite.missions_tracker",
        
        # Settings Theme
        "optimasite.countries",
        "optimasite.cities",
        "optimasite.currencies",
        "optimasite.languages",
        "optimasite.language_pack",
        
        # Configuration Theme
        "optimasite.permissions",
        "optimasite.statuses",
        "optimasite.genders",
        "optimasite.paymenttype",
        "optimasite.palettype",
        "optimasite.merchnature",
        "optimasite.settings",
        "optimasite.VAT",
        "optimasite.banner",
    ],
    
    # Icons for models
    "icons": {
        # Provider Theme Icons
        "optimasite.companies": "fas fa-building",
        "optimasite.companytypes": "fas fa-industry", 
        "optimasite.companyallservices": "fas fa-concierge-bell",
        "optimasite.companyservices": "fas fa-handshake",
        
        # Clients Theme Icons
        "optimasite.users": "fas fa-users",
        "optimasite.usertypes": "fas fa-user-tag",
        "optimasite.usersaddresses": "fas fa-map-marker-alt",
        "optimasite.tokens": "fas fa-key",
        
        # Vehicles Theme Icons
        "optimasite.vehicles": "fas fa-truck",
        "optimasite.vehiclecategories": "fas fa-list-alt",
        "optimasite.vehiclesalloptions": "fas fa-cogs",
        "optimasite.vehiclesoptions": "fas fa-tools",
        
        # Shipment Tracking Theme Icons
        "optimasite.carriers": "fas fa-ship",
        "optimasite.shipments": "fas fa-boxes",
        "optimasite.shipment_tags": "fas fa-tags",
        "optimasite.shipment_followers": "fas fa-user-friends",
        "optimasite.shipment_status_updates": "fas fa-route",
        "optimasite.broker_profiles": "fas fa-user-tie",
        "optimasite.notification_logs": "fas fa-bell",
        
        # Operations Theme Icons
        "optimasite.requests": "fas fa-clipboard-list",
        "optimasite.missions": "fas fa-tasks",
        "optimasite.attributions": "fas fa-link",
        "optimasite.requestoffers": "fas fa-hand-holding-usd",
        "optimasite.missions_tracker": "fas fa-map-marked-alt",
        
        # Settings Theme Icons
        "optimasite.countries": "fas fa-globe",
        "optimasite.cities": "fas fa-city",
        "optimasite.currencies": "fas fa-coins",
        "optimasite.languages": "fas fa-language",
        "optimasite.language_pack": "fas fa-file-alt",
        
        # Configuration Theme Icons
        "optimasite.permissions": "fas fa-lock",
        "optimasite.statuses": "fas fa-check-circle",
        "optimasite.genders": "fas fa-venus-mars",
        "optimasite.paymenttype": "fas fa-credit-card",
        "optimasite.palettype": "fas fa-pallet",
        "optimasite.merchnature": "fas fa-box-open",
        "optimasite.settings": "fas fa-sliders-h",
        "optimasite.VAT": "fas fa-percent",
        "optimasite.banner": "fas fa-image",
    },
    
    # Custom CSS
    "custom_css": None,
    "custom_js": None,
    
    # Show/hide elements
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    
    # Related modal
    "related_modal_active": False,
    
    # UI Tweaks
    "custom_links": {
        "optimasite": [
            {
                "name": "📊 Dashboard", 
                "url": "admin:index", 
                "icon": "fas fa-tachometer-alt"
            },
            {
                "name": "🚚 Quick Add Vehicle", 
                "url": "admin:optimasite_vehicles_add", 
                "icon": "fas fa-plus"
            },
            {
                "name": "📦 Quick Add Shipment", 
                "url": "admin:optimasite_shipments_add", 
                "icon": "fas fa-plus"
            },
        ]
    },
    
    # User menu on the right side
    "usermenu_links": [
        {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},
        {"model": "auth.user"}
    ],
}

# UI Tweaks for better organization
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-navy",
    "accent": "accent-primary",
    "navbar": "navbar-navy navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-navy",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "flatly",
    "dark_mode_theme": "darkly",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}
