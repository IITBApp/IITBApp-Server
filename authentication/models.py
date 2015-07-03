from django.db import models
from django.contrib.auth.models import User

class Designation(models.Model):
    user = models.ForeignKey(User)
    designation_name = models.CharField(max_length=128)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
