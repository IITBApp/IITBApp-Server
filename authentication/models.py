from django.db import models
from urlparse import urljoin
from iitbapp import notification
from django.conf import settings

# Create your models here.
class Registration(models.Model):
    email = models.EmailField(unique=True)
    token = models.TextField(null=True)
    active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super(Registration, self).save(*args, **kwargs)
        self.send_notification()

    def send_notification(self):
        link = "/api/registration/verify/?token=%s&email=%s&format=json" % (self.token, self.email)
        message = """
        Thanks for registering to IITB App, to verify your email visit following link

        %s

        Thanks and Regards,
        IITB App team
        """
        link = urljoin(settings.SERVER, link)
        message = message % link
        subject = "Verification email for IITB App"
        from_user = settings.EMAIL_FROM
        notification.send_mail(subject, message, from_user, [self.email])


