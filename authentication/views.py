from rest_framework import viewsets
from django.contrib.auth.models import User
from serializers import UserSerializer
import ldap
import json
from django.http import HttpResponse
from rest_framework.decorators import list_route
from models import UserToken
from forms import LogoutForm
import uuid
from tokenauth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from iitbapp.permissions import IsCorrectUserId


def authenticate_ldap(username, password, token):
    connection = ldap.initialize("ldap://ldap.iitb.ac.in")

    search_result = connection.search_s('dc=iitb,dc=ac,dc=in', ldap.SCOPE_SUBTREE, 'uid=%s' % username,
                                        ['uid', 'cn', 'givenName', 'sn', 'mail', 'employeeNumber'])

    response_data = {
        'error': False,
        'error_message': "",
        'first_name': "",
        'last_name': "",
        'email': "",
        'employeeNumber': "",
        'ldap': "",
        'name': "",
        'token': "",
    }

    if len(search_result) < 1 or search_result[0][1]['uid'][0] != username:
        response_data['error'] = True
        response_data['error_message'] = "Invalid Username/Password"
    else:
        result_dict = search_result[0][1]
        response_data['first_name'] = result_dict['givenName'][0]
        response_data['last_name'] = result_dict['sn'][0]
        response_data['name'] = result_dict['cn'][0]
        response_data['email'] = result_dict['mail'][0]
        response_data['ldap'] = result_dict['uid'][0]
        response_data['employeeNumber'] = result_dict['employeeNumber'][0]
        bind_ds = search_result[0][0]

        try:
            connection.bind_s(bind_ds, password)
            response_data['error'] = False
            user_serialized = UserSerializer(data=response_data)
            if user_serialized.is_valid():
                user = user_serialized.save()
                user.backend = "django.contrib.auth.backends.ModelBackend"
                response_data['id'] = user.id

                if token:
                    user_token = UserToken(user=user)
                    user_token.save()
                    response_data['token'] = user_token.token.hex

                return response_data, user
            else:
                response_data['error'] = True
                response_data['error_message'] = 'Unable to login. Please contact admin'
        except ldap.INVALID_CREDENTIALS:
            response_data['error'] = True
            response_data['error_message'] = "Invalid Credentials"

    return response_data, None


class UserViewset(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @list_route(methods=['POST'])
    def authenticate(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        response_data, user = authenticate_ldap(username, password, True)

        json_data = json.dumps(response_data)
        return HttpResponse(json_data, content_type="application/json")

    @list_route(methods=['POST'], authentication_classes=[TokenAuthentication],
                permission_classes=[IsAuthenticated, IsCorrectUserId])
    def logout(self, request):
        logout_form = LogoutForm(data=request.DATA)
        if logout_form.is_valid():
            user = logout_form.cleaned_data['user']
            self.check_object_permissions(request, user)
            logout_all = logout_form.cleaned_data['logout_all']
            token = request.META.get('HTTP_TOKEN_AUTH')
            if logout_all:
                UserToken.objects.all().filter(user=user).delete()
            else:
                UserToken.objects.all().filter(user=user).filter(token=uuid.UUID(token)).delete()
            return HttpResponse("{}", content_type="application/json")
        return HttpResponse(logout_form.errors.as_json(), content_type="application/json")
