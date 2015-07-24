__author__ = 'dheerenr'

from rest_framework import authentication, exceptions
from models import UserToken
import uuid


class TokenAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        token = request.META.get('HTTP_TOKEN_AUTH')
        if not token:
            return None
        else:
            try:
                uuid_token = uuid.UUID(token)
                user_token = UserToken.objects.all().filter(token=uuid_token)
                if user_token.exists():
                    user = user_token[0].user
                    return user, user_token
            except ValueError:
                pass
            raise exceptions.AuthenticationFailed('Invalid token')
