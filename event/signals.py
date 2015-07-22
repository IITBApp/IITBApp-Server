__author__ = 'dheerendra'

from serializers import EventReadSerializer
from models import Event
import logging
import json
from globals import send_android_push_notification
import django.dispatch

logger = logging.getLogger(__name__)


def create_message(instance, created):
    action = 'new' if created else 'update'
    message_dict = {
        'action': action,
        'type': 'event',
        'item': EventReadSerializer(instance).data,
    }
    return json.dumps(message_dict)


def send_event_push_notification(sender, instance, created, **kwargs):
    message = create_message(instance, created)
    send_android_push_notification(message)
    logger.info("Android push sent for event with id %d with message %s", instance.id, message)


event_done = django.dispatch.Signal(providing_args=['created', 'instance'])

event_done.connect(send_event_push_notification, Event)

