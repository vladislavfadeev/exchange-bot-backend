from django.apps import AppConfig


class WebAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.web_app'
    label = 'web_app'
    verbose_name = 'Telegram Web Application'


 