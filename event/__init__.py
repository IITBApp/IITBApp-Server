from django.apps import AppConfig

class EventAppConfig(AppConfig):

    name = 'event'

    def ready(self):
        import event.signals

default_app_config = 'event.EventAppConfig'