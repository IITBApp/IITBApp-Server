from django.db import models
import os
from uuid import uuid4
from authentication.models import Designation
from django.contrib.auth.models import User

# Create your models here.

def event_images(instance, filename):
    filename = filename.split('.')
    if len(filename) > 1:
        ext = filename[-1]
    else:
        ext = "jpg"
    return os.path.join("event_images", uuid4().hex + "." + ext)

class Event(models.Model):
    event_category = [('sport', 'SPORTS')]
    title = models.CharField(max_length=256)
    description = models.TextField()
    category = models.CharField(max_length=16, choices=event_category)
    event_time = models.DateTimeField()
    event_place = models.CharField(max_length=256)
    image = models.ImageField(null=True, upload_to=event_images)
    created = models.DateTimeField(auto_now_add=True)
    cancelled = models.BooleanField(default=False)
    posted_by = models.ForeignKey(Designation, related_name='events')


class EventLike(models.Model):
    event = models.ForeignKey(Event, related_name='likes')
    user = models.ForeignKey(User)

class EventViews(models.Model):
    event = models.ForeignKey(Event, related_name='views')
    user = models.ForeignKey(User)


