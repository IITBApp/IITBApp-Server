from django.db import models


class Information(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    logo = models.ImageField(upload_to='logos', null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    phone = models.CharField(max_length=16, null=True, blank=True)
    fax = models.CharField(max_length=16, null=True, blank=True)

    class Meta:
        abstract = True

class Contact(Information):
    pass

class Department(Information):
    pass

class Club(Information):
    pass

class EmergencyContact(Information):
    pass


