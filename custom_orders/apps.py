from django.apps import AppConfig


class CustomOrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'custom_orders'
    
    def ready(self):
        import custom_orders.translations