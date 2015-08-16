__author__ = 'dheerendra'

from django.core.management.base import BaseCommand
from feed.models import FeedConfig
import sys
from fractions import gcd
from crontab import CronTab
from core.management.configuration import write_to_stdout
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Add feed checking cron job'
    comment = 'CHECK_FEED_CRON'
    check_command = 'check_feeds'

    def add_arguments(self, parser):
        parser.add_argument('--delete',
                            action='store_true',
                            dest='delete',
                            default=False,
                            help='Delete all feed cron jobs')

    def handle(self, *args, **options):
        cron_tab = CronTab()
        cron_tab.remove_all(comment=self.comment)

        if options['delete']:
            write_to_stdout('Deleted all feed cron jobs\n')

        else:
            feed_configs = FeedConfig.objects.all().values('check_frequency')
            frequencies = [config.get('check_frequency') for config in feed_configs]
            gcd_frequencies = reduce(gcd, frequencies)
            executable = sys.executable
            manage_py_path = os.path.join(settings.BASE_DIR, 'manage.py')
            command = "%s %s %s" % (executable, manage_py_path, self.check_command)

            job = cron_tab.new(command=command, comment=self.comment)
            job.minute.every(gcd_frequencies)
            write_to_stdout('Added %s in cron for every %d minutes\n' % (command, gcd_frequencies))
        cron_tab.write()
