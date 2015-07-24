from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Designation(models.Model):
    user = models.ForeignKey(User, related_name='designations')
    post = models.CharField(max_length=128)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

    def is_active(self):
        curr_date = datetime.now().date()
        if self.start_date <= curr_date <= self.end_date:
            return True
        return False

    def __unicode__(self):
        return self.user.username + "-" + self.post
