# optimasite/context_processors.py
from django.conf import settings

def firebase_config(request):
    """Context processor pour la configuration Firebase"""
    return {
        'firebase_config': getattr(settings, 'FIREBASE_WEB_CONFIG', {}),
        'notification_settings': getattr(settings, 'NOTIFICATION_SETTINGS', {}),
    }
