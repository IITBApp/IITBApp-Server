from django.db import models
from authentication.models import Designation
from gcm.models import get_device_model
from django.db.models import signals
import logging

logger = logging.getLogger(__name__)

notice_priority = [('0', 'Low'), ('1', 'Medium'), ('2', 'High'), ('3', 'Urgent')]

class Notice(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=256)
    description = models.TextField()
    priority = models.CharField(max_length=1, choices=notice_priority)
    expiration_date = models.DateTimeField(null=True)
    posted_by = models.ForeignKey(Designation)

def send_gcm_for_notice(sender, instance, created, **kwargs):
    action = 'save' if created else 'update'
    Device = get_device_model()
    Device.objects.all().send_message('New notice is added')
    logger.info("signal triggered")

signals.post_save.connect(send_gcm_for_notice, Notice)


