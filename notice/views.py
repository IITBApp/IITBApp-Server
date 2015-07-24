from rest_framework import viewsets
from serializers import NoticeReadSerializer
from models import Notice
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from authentication.tokenauth import TokenAuthentication


class NoticePagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 50


class NoticeViewset(viewsets.ReadOnlyModelViewSet):

    queryset = Notice.objects.all().order_by('-id')
    pagination_class = NoticePagination
    serializer_class = NoticeReadSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
