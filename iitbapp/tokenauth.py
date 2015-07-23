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
        if token != settings.TOKEN_AUTH:
            return None
#            raise exceptions.AuthenticationFailed('Invalid Token')

        return (User.objects.get(username=settings.SUPERUSER), None)