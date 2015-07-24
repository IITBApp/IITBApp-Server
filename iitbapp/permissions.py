__author__ = 'dheerendra'

from rest_framework.permissions import BasePermission


class IsCorrectUserId(BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.id == obj:
            return True
        return False
