import os
from uuid import uuid4

from django.db import models
from django.contrib.auth.models import User

from authentication.models import Designation
from core.globals import categories


def event_images(instance, filename):
    filename = filename.split('.')
    if len(filename) > 1:
        ext = filename[-1]
    else:
        ext = "jpg"
    return os.path.join("event_images", uuid4().hex + "." + ext)


class Event(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    category = models.CharField(max_length=16, choices=categories)
    event_time = models.DateTimeField()
    event_place = models.CharField(max_length=256)
    time = models.DateTimeField(auto_now_add=True)
    cancelled = models.BooleanField(default=False)
    posted_by = models.ForeignKey(Designation, related_name='events')

    def __unicode__(self):
        return self.title


class EventImage(models.Model):
    event = models.ForeignKey(Event, related_name='images')
    image = models.ImageField(upload_to=event_images)

    def __unicode__(self):
        return self.image.url


class EventLike(models.Model):
    event = models.ForeignKey(Event, related_name='likes')
    user = models.ForeignKey(User)


class EventViews(models.Model):
    event = models.ForeignKey(Event, related_name='views')
    user = models.ForeignKey(User)
