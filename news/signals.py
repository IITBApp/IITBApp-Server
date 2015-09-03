__author__ = 'dheerendra'

import logging
import json

import django.dispatch

from serializers import NewsReadSerializer
from models import News
from core.globals import send_android_push_notification
from pns import pns

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
    pns.send_pns(message)
    logger.info("Android push sent for news with id %d with message %s to new devices", instance.id, message)


news_done = django.dispatch.Signal(providing_args=['instance', 'created'])
news_done.connect(send_news_push_notification, News)
