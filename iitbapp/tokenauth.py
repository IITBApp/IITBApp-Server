__author__ = 'dheerenr'

from rest_framework import authentication
from django.contrib.auth.models import User
from django.conf import settings


class TokenAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        token = request.META.get('HTTP_TOKEN')
        if not token:
            return None
        if token != settings.TOKEN_AUTH:
            return None

        return User.objects.get(username=settings.SUPERUSER), None
