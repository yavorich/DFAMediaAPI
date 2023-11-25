from django.apps import AppConfig


class ShopApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop_api'

    def ready(self) -> None:
        import shop_api.signals
