from django.db import models
from django.contrib.auth.models import User

class Feed(models.Model):

    guid = models.CharField(max_length=128)
    user = models.ForeignKey(User)

    class Meta:
        abstract = True


class FeedLike(Feed):
    pass


class FeedView(Feed):
    pass
