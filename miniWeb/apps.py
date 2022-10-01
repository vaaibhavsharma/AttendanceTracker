from django.apps import AppConfig


class MiniwebConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'miniWeb'
    def ready(self):
        import miniWeb.signals
