from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4
from authentication.models import Designation
from globals import categories
import os


def news_images(instance, filename):
    filename = filename.split('.')
    if len(filename) > 1:
        ext = filename[-1]
    else:
        ext = "jpg"
    return os.path.join("news_images", uuid4().hex + "." + ext)


class News(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=512)
    description = models.TextField()
    category = models.CharField(max_length=16, choices=categories)
    posted_by = models.ForeignKey(Designation, related_name='news')
    published = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = "news"


class NewsImage(models.Model):
    news = models.ForeignKey(News, related_name='images')
    image = models.ImageField(upload_to=news_images)

    def __unicode__(self):
        return self.image.url


class NewsLike(models.Model):
    news = models.ForeignKey(News, related_name='likes')
    user = models.ForeignKey(User)


class NewsViews(models.Model):
    news = models.ForeignKey(News, related_name='views')
    user = models.ForeignKey(User)
