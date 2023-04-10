from django.apps import AppConfig


class MentosAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MentOS_app'

    def ready(self):
        import MentOS_app.signals
