from django.apps import AppConfig


class OptimasiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'optimasite'
    def ready(self):
        import optimasite.signals
