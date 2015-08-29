__author__ = 'dheerendra'
'''
This file is for migrating from django-gcm to inbuilt gcm.
Delete it after sometime (When all users have moved from old gcm to new gcm tables)

On save mark the old device as inactive. All new users should be registered in new table only.
'''

from gcm.models import get_device_model
from django.db.models import signals
from .models import Device


def manage_gcm(sender, instance, created, **kwargs):
    if created:
        dev_id = instance.dev_id
        old_devices = get_device_model()
        old_devices.objects.all().filter(dev_id=dev_id).update(is_active=False)

signals.post_save.connect(manage_gcm, Device)

