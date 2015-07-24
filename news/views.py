from rest_framework import viewsets
from models import News, NewsLike, NewsViews
from serializers import NewsReadSerializer, NewsLikeSerializer, NewsViewSerializer
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.pagination import LimitOffsetPagination


class NewsPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 50


class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = News.objects.all().order_by('-id')
    pagination_class = NewsPagination
    serializer_class = NewsReadSerializer

    @list_route(methods=['POST'])
    def like(self, request):
        serializer = NewsLikeSerializer(data=request.data)
        if serializer.is_valid():
            news = serializer.data['news']
            user = serializer.data['user']
            news_like, created = NewsLike.objects.get_or_create(news__id=news, user__id=user,
                                                                defaults={'news_id': news, 'user_id': user})
            return Response(NewsLikeSerializer(news_like, context={'liked': created}).data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'])
    def unlike(self, request):
        serializer = NewsLikeSerializer(data=request.data)
        if serializer.is_valid():
            news = serializer.data['news']
            user = serializer.data['user']
            NewsLike.objects.all().filter(news=news).filter(user=user).delete()
            likes = NewsLike.objects.all().filter(news=news).count()
            return Response({'status': 'deleted', 'likes': likes})
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'])
    def view(self, request):
        serializer = NewsViewSerializer(data=request.data)
        if serializer.is_valid():
            news = serializer.data['news']
            user = serializer.data['user']
            news_view, created = NewsViews.objects.get_or_create(news__id=news, user_id=user,
                                                                 defaults={'news_id': news, 'user_id': user})
            return Response(NewsViewSerializer(news_view, context={'viewed': created}).data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
