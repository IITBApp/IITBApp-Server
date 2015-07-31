from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone


class Designation(models.Model):
    user = models.ForeignKey(User, related_name='designations')
    post = models.CharField(max_length=128)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

    def is_active(self):
        curr_date = timezone.now().date()
        if self.start_date <= curr_date <= self.end_date:
            return True
        return False

    def __unicode__(self):
        return self.user.username + "-" + self.post


class UserToken(models.Model):
    user = models.ForeignKey(User)
    token = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    last_accessed = models.DateTimeField(default=timezone.now)
    has_expired = models.BooleanField(default=False)

    def is_active(self):
        if self.has_expired:
            return False
        curr_date = timezone.now()
        diff = abs((curr_date - self.last_accessed).days)
        if (diff > 30):
            self.has_expired = True
            self.save()
            return False
        else:
            self.last_accessed = curr_date
            self.save()
            return True
