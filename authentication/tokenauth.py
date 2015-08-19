__author__ = 'dheerenr'

from rest_framework import authentication, exceptions
from models import UserToken
import uuid


class TokenAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        token = request.META.get('HTTP_TOKEN_AUTH') or request.query_params.get('token-auth')
        if not token:
            return None
        else:
            try:
                uuid_token = uuid.UUID(token)
                user_token = UserToken.objects.all().filter(token=uuid_token)
                if user_token.exists():
                    user_token = user_token[0]
                    if user_token.is_active():
                        user = user_token.user
                        return user, user_token
                    else:
                        pass
            except ValueError:
                pass
            raise exceptions.AuthenticationFailed('Invalid token')
