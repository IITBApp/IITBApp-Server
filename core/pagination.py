__author__ = 'dheerendra'

from rest_framework.pagination import LimitOffsetPagination


class DefaultLimitOffsetPagination(LimitOffsetPagination):

    default_limit = 20
    max_limit = 50
