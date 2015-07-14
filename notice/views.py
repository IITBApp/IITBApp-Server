from rest_framework import viewsets
from serializers import NoticeWriteSerializer, NoticeReadSerializer
from models import Notice
from rest_framework.pagination import LimitOffsetPagination


class NoticePagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 50

class NoticeViewset(viewsets.ModelViewSet):

    queryset = Notice.objects.all()
    pagination_class = NoticePagination

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return NoticeWriteSerializer
        else:
            return NoticeReadSerializer

