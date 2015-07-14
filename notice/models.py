from django.db import models
from authentication.models import Designation

# Create your models here.

notice_priority = [('0', 'Low'), ('1', 'Medium'), ('2', 'High'), ('3', 'Urgent')]

class Notice(models.Model):
    issue_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=256)
    description = models.TextField()
    priority = models.CharField(max_length=1, choices=notice_priority)
    expiration_date = models.DateTimeField(null=True)
    posted_by = models.ForeignKey(Designation)
