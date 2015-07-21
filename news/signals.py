__author__ = 'dheerendra'

from serializers import NewsReadSerializer
from models import News
from django.db.models import signals
import logging
import json
from globals import send_android_push_notification

logger = logging.getLogger(__name__)


def create_message(instance, created):
    action = 'new' if created else 'update'
    message_dict = {
        'action': action,
        'type': 'news',
        'item': NewsReadSerializer(instance).data,
    }
    return json.dumps(message_dict)


def send_news_push_notification(sender, instance, created, **kwargs):
    message = create_message(instance, created)
    send_android_push_notification(message)
    logger.info("Android push sent for news with id %d with message %s", instance.id, message)


signals.post_save.connect(send_news_push_notification, News)
