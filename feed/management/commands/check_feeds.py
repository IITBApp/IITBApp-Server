__author__ = 'dheerendra'

from django.core.management.base import BaseCommand
from feed.models import FeedConfig
from core.management.configuration import write_to_stdout


class Command(BaseCommand):

    help = 'Check feed for all feed configurations'

    def handle(self, *args, **options):

        feed_configs = FeedConfig.objects.all()
        for feed_config in feed_configs:
            write_to_stdout("Started feed check for %s\n" % feed_config.title)
            feed_config.check_feeds()
            write_to_stdout("Finished feed check for %s\n\n" % feed_config.title)
