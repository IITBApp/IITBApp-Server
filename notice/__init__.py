from django.apps import AppConfig

class NoticeAppConfig(AppConfig):

    name = 'notice'

    def ready(self):
        import notice.signals

default_app_config = 'notice.NoticeAppConfig'