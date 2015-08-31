from django.apps import AppConfig


class FeedAppConfig(AppConfig):

    name = 'feed'

    def ready(self):
        import feed.feed_pns

default_app_config = 'feed.FeedAppConfig'