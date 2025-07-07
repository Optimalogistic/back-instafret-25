# optimasite/services/fcm_service.py

import firebase_admin
from firebase_admin import credentials, messaging
from django.conf import settings
from django.contrib.auth import get_user_model
from optimasite.models import device_tokens
import logging
import threading
import time
from typing import List, Dict, Optional, Union

logger = logging.getLogger(__name__)

class FCMService:
    """Service Firebase Cloud Messaging amélioré pour les notifications admin"""
    
    _instance = None
    _app = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FCMService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._app:
            self._initialize_firebase()
    
    def _initialize_firebase(self):
        """Initialise Firebase Admin SDK"""
        try:
            if not firebase_admin._apps:
                if settings.FIREBASE_ADMIN_CRED:
                    cred = credentials.Certificate(settings.FIREBASE_ADMIN_CRED)
                    self._app = firebase_admin.initialize_app(cred)
                    logger.info("Firebase Admin SDK initialisé avec succès")
                else:
                    logger.error("FIREBASE_ADMIN_CRED non configuré")
            else:
                self._app = firebase_admin.get_app()
        except Exception as e:
            logger.error(f"Erreur initialisation Firebase: {e}")
            raise
    
    def get_user_tokens(self, users) -> List[str]:
        """Récupère tous les tokens actifs pour une liste d'utilisateurs"""
        if not users:
            return []
        
        # Convertir en liste si c'est un QuerySet
        if hasattr(users, '__iter__') and not isinstance(users, (str, dict)):
            user_list = list(users)
        else:
            user_list = [users] if not isinstance(users, list) else users
        
        # Extraire les IDs des utilisateurs
        user_ids = []
        for user in user_list:
            if hasattr(user, 'id'):
                user_ids.append(user.id)
            elif isinstance(user, (int, str)):
                user_ids.append(user)
        
        if not user_ids:
            return []
        
        tokens = device_tokens.objects.filter(
            user_id__in=user_ids,
            is_active=True
        ).values_list('token', flat=True)
        
        return list(tokens)
    
    def send_notification_with_sound(
        self, 
        tokens: List[str], 
        title: str, 
        body: str, 
        data: Optional[Dict] = None,
        sound: str = "notification.mp3",
        priority: str = "high"
    ) -> Dict:
        """Envoie une notification avec son personnalisé"""
        
        if not tokens:
            return {"success": False, "error": "Aucun token fourni"}
        
        # Préparer les données de notification
        notification_data = data or {}
        notification_data.update({
            "click_action": "FLUTTER_NOTIFICATION_CLICK",
            "sound": sound,
            "priority": priority,
            "timestamp": str(int(time.time()))
        })
        
        try:
            # Configuration du message avec son et priorité
            message = messaging.MulticastMessage(
                notification=messaging.Notification(
                    title=title,
                    body=body,
                ),
                data=notification_data,
                tokens=tokens,
                android=messaging.AndroidConfig(
                    notification=messaging.AndroidNotification(
                        sound=sound.replace('.mp3', '').replace('.wav', ''),
                        channel_id="admin_notifications",
                        priority="high",
                        default_sound=False,
                        default_vibrate_timings=False,
                        vibrate_timings_millis=[200, 100, 200]
                    ),
                    priority="high"
                ),
                apns=messaging.APNSConfig(
                    payload=messaging.APNSPayload(
                        aps=messaging.Aps(
                            sound=sound.replace('.mp3', '.wav'),
                            badge=1,
                            alert=messaging.ApsAlert(
                                title=title,
                                body=body
                            )
                        )
                    ),
                    headers={"apns-priority": "10"}
                ),
                webpush=messaging.WebpushConfig(
                    notification=messaging.WebpushNotification(
                        title=title,
                        body=body,
                        icon="/static/admin/img/notification-icon.png",
                        badge="/static/admin/img/badge-icon.png",
                        sound=f"/static/sounds/{sound}",
                        require_interaction=True
                    ),
                    headers={"Urgency": "high"}
                )
            )
            
            response = messaging.send_multicast(message)
            
            # Log des résultats
            logger.info(f"Notifications envoyées: {response.success_count}/{len(tokens)}")
            
            if response.failure_count > 0:
                logger.warning(f"Échecs d'envoi: {response.failure_count}")
                self._cleanup_invalid_tokens(tokens, response.responses)
            
            return {
                "success": True,
                "success_count": response.success_count,
                "failure_count": response.failure_count,
                "total_tokens": len(tokens)
            }
            
        except Exception as e:
            logger.error(f"Erreur envoi notification FCM: {e}")
            return {"success": False, "error": str(e)}
    
    def _cleanup_invalid_tokens(self, tokens: List[str], responses: List):
        """Nettoie les tokens invalides après un envoi"""
        try:
            invalid_tokens = []
            for i, response in enumerate(responses):
                if not response.success:
                    error_code = response.exception.code if response.exception else None
                    if error_code in ['INVALID_REGISTRATION_TOKEN', 'UNREGISTERED']:
                        invalid_tokens.append(tokens[i])
            
            if invalid_tokens:
                deleted_count = device_tokens.objects.filter(
                    token__in=invalid_tokens
                ).update(is_active=False)
                logger.info(f"Désactivé {deleted_count} tokens invalides")
                
        except Exception as e:
            logger.error(f"Erreur nettoyage tokens: {e}")
    
    def send_to_admins(
        self, 
        title: str, 
        body: str, 
        notification_type: str = "admin",
        data: Optional[Dict] = None,
        sound: str = "admin_notification.mp3"
    ) -> Dict:
        """Envoie une notification à tous les administrateurs"""
        
        User = get_user_model()
        admin_users = User.objects.filter(is_superuser=True, is_active=True)
        
        if not admin_users.exists():
            return {"success": False, "error": "Aucun administrateur trouvé"}
        
        tokens = self.get_user_tokens(admin_users)
        
        if not tokens:
            return {"success": False, "error": "Aucun token admin trouvé"}
        
        # Enrichir les données
        notification_data = data or {}
        notification_data.update({
            "type": notification_type,
            "target": "admin",
            "admin_notification": "true"
        })
        
        return self.send_notification_with_sound(
            tokens=tokens,
            title=title,
            body=body,
            data=notification_data,
            sound=sound,
            priority="high"
        )

# Instance globale du service
fcm_service = FCMService()

def push_to_users(user_queryset, title: str, body: str, data: Optional[Dict] = None) -> int:
    """Fonction helper pour maintenir la compatibilité avec l'ancien code"""
    try:
        tokens = fcm_service.get_user_tokens(user_queryset)
        
        if not tokens:
            logger.warning("Aucun token trouvé pour les utilisateurs")
            return 0
        
        result = fcm_service.send_notification_with_sound(
            tokens=tokens,
            title=title,
            body=body,
            data=data
        )
        
        return result.get("success_count", 0) if result["success"] else 0
        
    except Exception as e:
        logger.error(f"Erreur dans push_to_users: {e}")
        return 0

def notify_new_user(user_instance):
    """Notification spécifique pour nouvel utilisateur"""
    return fcm_service.send_to_admins(
        title="🆕 Nouveau Utilisateur",
        body=f"{user_instance.username} vient de s'inscrire sur la plateforme",
        notification_type="new_user",
        data={
            "user_id": str(user_instance.id),
            "url": f"/admin/optimasite/users/{user_instance.id}/change/",
            "action": "view_user"
        },
        sound="new_user.mp3"
    )

def notify_new_request(request_instance):
    """Notification spécifique pour nouvelle demande"""
    return fcm_service.send_to_admins(
        title="📋 Nouvelle Demande",
        body=f"Demande {request_instance.Rref} créée par {request_instance.user.username}",
        notification_type="new_request",
        data={
            "request_id": str(request_instance.id),
            "url": f"/admin/optimasite/requests/{request_instance.id}/change/",
            "action": "view_request"
        },
        sound="new_request.mp3"
    )

def notify_status_update(request_instance, old_status: str, new_status: str):
    """Notification pour changement de statut"""
    user_tokens = fcm_service.get_user_tokens([request_instance.user])
    
    if not user_tokens:
        return {"success": False, "error": "Aucun token utilisateur"}
    
    return fcm_service.send_notification_with_sound(
        tokens=user_tokens,
        title="🔄 Statut Mis à Jour",
        body=f"Votre demande {request_instance.Rref} est maintenant: {new_status}",
        data={
            "request_id": str(request_instance.id),
            "old_status": old_status,
            "new_status": new_status,
            "url": f"/requests/{request_instance.id}/",
            "action": "view_request",
            "type": "status_update"
        },
        sound="status_update.mp3"
    )

def notify_new_offer(offer_instance):
    """Notification pour nouvelle offre"""
    user_tokens = fcm_service.get_user_tokens([offer_instance.request.user])
    
    if not user_tokens:
        return {"success": False, "error": "Aucun token utilisateur"}
    
    return fcm_service.send_notification_with_sound(
        tokens=user_tokens,
        title="💰 Nouvelle Offre",
        body=f"{offer_instance.company.name} propose {offer_instance.value} pour votre demande {offer_instance.request.Rref}",
        data={
            "offer_id": str(offer_instance.id),
            "request_id": str(offer_instance.request.id),
            "company_id": str(offer_instance.company.id),
            "url": f"/offers/{offer_instance.id}/",
            "action": "view_offer",
            "type": "new_offer"
        },
        sound="new_offer.mp3"
    )

def test_admin_notification():
    """Fonction de test pour vérifier que les notifications admin fonctionnent"""
    return fcm_service.send_to_admins(
        title="🧪 Test Notification",
        body="Ceci est un test du système de notifications admin",
        notification_type="test",
        data={"test": "true"},
        sound="test_notification.mp3"
    )
