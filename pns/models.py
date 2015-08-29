import logging

from django.db import models
from django.contrib.auth.models import User
from django.db.models.query import QuerySet

from . import gcm_api

logger = logging.getLogger(__name__)


class GCMMessage(gcm_api.GCMMessage):
    GCM_INVALID_ID_ERRORS = ['InvalidRegistration',
                             'NotRegistered',
                             'MismatchSenderId']

    def send(self, regs_id, data, **kwargs):
        response = super(GCMMessage, self).send(regs_id, data, **kwargs)
        chunks = [response] if not isinstance(response, list) else response
        for chunk in chunks:
            self.post_send(*chunk)
        return response

    def post_send(self, regs_id, response):
        if response['failure']:
            invalid_messages = dict(filter(
                lambda x: x[1].get('error') in self.GCM_INVALID_ID_ERRORS,
                zip(regs_id, response.get('results'))))

            regs = list(invalid_messages.keys())
            for device in Device.objects.filter(reg_id__in=regs):
                device.mark_inactive(
                    error_message=invalid_messages[device.reg_id]['error'])


class DeviceQuerySet(QuerySet):

    def send_message(self, data, **kwargs):
        if self:
            return GCMMessage().send(
                regs_id=list(self.values_list("reg_id", flat=True)),
                data=data, **kwargs)


class DeviceManager(models.Manager):

    def get_queryset(self):
        return DeviceQuerySet(self.model)


class Device(models.Model):
    dev_id = models.CharField(max_length=50, verbose_name="Device Id", unique=True)
    reg_id = models.CharField(max_length=256, verbose_name="Registration Id")
    user = models.ForeignKey(User)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    objects = DeviceManager()

    def __unicode__(self):
        return self.dev_id

    def mark_inactive(self, **kwargs):
        self.is_active = False
        self.save()
        if kwargs.get('error_message'):
            logger.debug("Device %s (%s) marked inactive due to error: %s",
                         self.dev_id, self.user, kwargs['error_message'])