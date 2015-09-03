from django.apps import AppConfig


class FeedAppConfig(AppConfig):

    name = 'feed'

    def ready(self):
        import feed.signals_receivers

default_app_config = 'feed.FeedAppConfig'