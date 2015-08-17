__author__ = 'dheerendra'

from serializers import FeedEntrySerializer, FeedConfigSerializer
from models import FeedEntry
from django.db.models import signals
import logging
import json
from core.globals import send_android_push_notification

logger = logging.getLogger(__name__)


def create_message(instance, created):
    instance.refresh_from_db()
    action = 'new' if created else 'update'
    feed_config_data = FeedConfigSerializer(instance.feed_config).data
    feed_entry_data = [FeedEntrySerializer(instance).data]
    feed_config_data['entries'] = feed_entry_data
    message_dict = {
        'action': action,
        'type': 'feed',
        'item': feed_config_data,
    }
    return json.dumps(message_dict)


def send_feed_push_notification(sender, instance, created, **kwargs):
    message = create_message(instance, created)
    send_android_push_notification(message)
    logger.info("Android push sent for feed with id %d with title %s", instance.id, instance.title)


signals.post_save.connect(send_feed_push_notification, FeedEntry)