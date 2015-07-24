from rest_framework import viewsets
from django.contrib.auth.models import User
from serializers import UserSerializer
import ldap
import json
from django.http import HttpResponse
from rest_framework.decorators import list_route


def authenticate_ldap(username, password):
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
        except ldap.INVALID_CREDENTIALS:
            response_data['error'] = True
            response_data['error_message'] = "Invalid Credentials"

    return response_data


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @list_route(methods=['POST'])
    def authenticate(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        response_data = authenticate_ldap(username, password)

        json_data = json.dumps(response_data)
        return HttpResponse(json_data, content_type="application/json")
