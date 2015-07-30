from django.db import models
from django.contrib.auth.models import User


class BugTracker(models.Model):
    phone_model = models.CharField(max_length=128)
    android_version = models.CharField(max_length=16)
    manufacturer = models.CharField(max_length=128)
    device_id = models.CharField(max_length=128)
    description = models.TextField()
    user = models.ForeignKey(User)
