from django.apps import AppConfig

class NewsAppConfig(AppConfig):

    name = 'news'

    def ready(self):
        import news.signals

default_app_config = 'news.NewsAppConfig'