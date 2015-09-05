from models import Device
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)


def send_pns(message, user_queryset=User.objects.all()):
    devices = Device.objects.all().filter(is_active=True)
    devices = devices.filter(user__in=user_queryset)
    devices.send_message(message)
    logger.info('Send new Android notification to %d users and %d devices' % (len(user_queryset), len(devices)))
