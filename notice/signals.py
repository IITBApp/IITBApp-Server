__author__ = 'dheerendra'

import logging
import json

import django.dispatch

from serializers import NoticeReadSerializer
from core.globals import send_android_push_notification
from models import Notice
from pns import pns

logger = logging.getLogger(__name__)


def create_message(instance, created):
    action = 'new' if created else 'update'
    message_dict = {
        'action': action,
        'type': 'notice',
        'item': NoticeReadSerializer(instance).data,
    }
    return json.dumps(message_dict)


def send_notice_push_notification(sender, instance, created, **kwargs):
    message = create_message(instance, created)
    send_android_push_notification(message)
    logger.info("Android push sent for notice with id %d with message %s", instance.id, message)
    pns.send_pns(message)
    logger.info("Android push sent for notice with id %d with message %s to new devices", instance.id, message)


notice_done = django.dispatch.Signal(providing_args=['instance', 'created'])
notice_done.connect(send_notice_push_notification, Notice)
