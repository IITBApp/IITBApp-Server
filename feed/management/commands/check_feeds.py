__author__ = 'dheerendra'

from django.core.management.base import BaseCommand, CommandError
from feed.models import FeedConfig
import sys


class Command(BaseCommand):

    help = 'Check feed for all feed configurations'

    def handle(self, *args, **options):

        feed_configs = FeedConfig.objects.all()
        for feed_config in feed_configs:
            sys.stdout.write("Started feed check for %s\n" % feed_config.title)
            sys.stdout.flush()
            feed_config.check_feeds()
            sys.stdout.write("Finished feed check for %s\n\n" % feed_config.title)
            sys.stdout.flush()
