from django.db import models
from authentication.models import Designation
from globals import notice_priority


class Notice(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=256)
    description = models.TextField()
    priority = models.CharField(max_length=1, choices=notice_priority)
    expiration_date = models.DateTimeField(null=True, blank=True)
    posted_by = models.ForeignKey(Designation)
