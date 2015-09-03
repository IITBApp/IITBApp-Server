__author__ = 'dheerendra'

from models import Device
from django.contrib.auth.models import User


def send_pns(message, user_queryset=User.objects.all()):
    devices = Device.objects.all().filter(is_active=True)
    devices = devices.filter(user__in=user_queryset)
    devices.send_message(message)
