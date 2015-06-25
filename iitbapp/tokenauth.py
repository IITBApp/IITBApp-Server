__author__ = 'dheerenr'

from rest_framework import authentication
from rest_framework import exceptions
from django.contrib.auth.models import User
from django.conf import settings

class TokenAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        token = request.META.get('HTTP_TOKEN')
        if not token:
            return None
#            raise exceptions.AuthenticationFailed('Token is not present')
        if token != "ctE6NBxTfO9DE1a0onCDcJfyZyMhAQXqgCknqNz8Q":
            return None
#            raise exceptions.AuthenticationFailed('Invalid Token')

        return (User.objects.get(username=settings.SUPERUSER), None)