__author__ = 'dheerendra'

from rest_framework import permissions


class UserIsForeignKey(permissions.BasePermission):

    def __init__(self, user_field_name='user'):
        super(UserIsForeignKey, self).__init__()
        self.user_field_name = user_field_name

    def has_object_permission(self, request, view, obj):
        user = getattr(obj, self.user_field_name, None)
        if user == request.user:
            return True
        return False
