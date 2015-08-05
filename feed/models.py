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
    view_count = models.IntegerField(default=0)

    def add_view(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])
