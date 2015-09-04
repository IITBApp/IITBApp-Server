__author__ = 'dheerendra'

from django.core.management.base import BaseCommand
from feed.models import FeedConfig
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Check feed for all feed configurations'

    def handle(self, *args, **options):

        feed_configs = FeedConfig.objects.all()
        for feed_config in feed_configs:
            logger.info("Started feed check for %s" % feed_config.title)
            feed_config.check_feeds()
            logger.info("Finished feed check for %s" % feed_config.title)
