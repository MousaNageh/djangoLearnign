from django.apps import AppConfig


class ApiAppConfig(AppConfig):
    name = 'api_app'
    def ready(self):
        import api_app.signals