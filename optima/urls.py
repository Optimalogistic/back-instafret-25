"""optima URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from optimasite import views as optimasite_views
import os


urlpatterns = [
    path('optimasite/', include('optimasite.urls')),
    path('api/', include('optimasite.urls')),  # Assurez-vous que cette ligne existe
    # URLs directes pour les notifications (ajouter ces lignes)
    path('admin/test-notifications/', optimasite_views.test_notification, name='admin-test-notifications'),
    path('admin/notification-settings/', optimasite_views.notification_statistics, name='admin-notification-settings'),    
    # Service worker Firebase à la racine
    path('firebase-messaging-sw.js', serve, {
        'document_root': os.path.join(settings.BASE_DIR, 'optimasite', 'static'),
        'path': 'firebase-messaging-sw.js'
    }),
    path('admin/', admin.site.urls),
    
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

# Servir les fichiers statiques en développement
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    