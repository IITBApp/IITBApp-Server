from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from serializers import NoticeReadSerializer
from models import Notice
from authentication.tokenauth import TokenAuthentication
from core.pagination import DefaultLimitOffsetPagination


class NoticeViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Notice.objects.all().order_by('-id')
    pagination_class = DefaultLimitOffsetPagination
    serializer_class = NoticeReadSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
