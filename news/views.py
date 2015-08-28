from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticated
from django.db.models import Prefetch

from models import News, NewsLike, NewsViews
from serializers import NewsReadSerializer, NewsIdSerializer
from authentication.tokenauth import TokenAuthentication
from core.pagination import DefaultLimitOffsetPagination


class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = News.objects.all().order_by('-id')
    pagination_class = DefaultLimitOffsetPagination
    serializer_class = NewsReadSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = News.objects.all().order_by('-id').prefetch_related(
            Prefetch('likes', NewsLike.objects.all().filter(user=user), 'liked')
        ).prefetch_related(
            Prefetch('views', NewsViews.objects.all().filter(user=user), 'viewed')
        )
        return queryset

    @list_route(methods=['POST'])
    def like(self, request):
        serializer = NewsIdSerializer(data=request.data)
        if serializer.is_valid():
            news_id = serializer.data['news']
            NewsLike.objects.get_or_create(news_id=news_id, user=request.user)
            news = self.get_queryset().filter(id=news_id).first()
            return Response(NewsReadSerializer(news).data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'])
    def unlike(self, request):
        serializer = NewsIdSerializer(data=request.data)
        if serializer.is_valid():
            news_id = serializer.data['news']
            NewsLike.objects.all().filter(news=news_id).filter(user=request.user).delete()
            news = self.get_queryset().filter(id=news_id).first()
            return Response(NewsReadSerializer(news).data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'])
    def view(self, request):
        serializer = NewsIdSerializer(data=request.data)
        if serializer.is_valid():
            news_id = serializer.data['news']
            news_view, created = NewsViews.objects.get_or_create(news_id=news_id, user=request.user)
            news_view.add_view()
            news = self.get_queryset().filter(id=news_id).first()
            return Response(NewsReadSerializer(news).data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
