# optimasite/signals.py
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import users, requests, requestoffers
from .services.fcm_service import notify_new_user, notify_new_request, notify_status_update, notify_new_offer
from django.contrib.auth import get_user_model
import threading

@receiver(post_save, sender=users)
def notif_new_user(sender, instance, created, **kwargs):
    if created:
        def send_notification():
            notify_new_user(instance)
        
        threading.Thread(target=send_notification).start()

@receiver(post_save, sender=requests)
def notif_new_request(sender, instance, created, **kwargs):
    if created:
        def send_notification():
            notify_new_request(instance)
        
        threading.Thread(target=send_notification).start()
    
    else:
        # Vérifier si le statut a changé
        if hasattr(instance, '_state') and instance._state.adding is False:
            try:
                old_instance = requests.objects.get(pk=instance.pk)
                if old_instance.state != instance.state:
                    def send_status_notification():
                        notify_status_update(instance, str(old_instance.state), str(instance.state))
                    
                    threading.Thread(target=send_status_notification).start()
            except requests.DoesNotExist:
                pass

@receiver(post_save, sender=requestoffers)
def notif_new_offer(sender, instance, created, **kwargs):
    if created:
        def send_notification():
            notify_new_offer(instance)
        
        threading.Thread(target=send_notification).start()
