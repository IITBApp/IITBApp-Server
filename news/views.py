from rest_framework import viewsets
from models import News, NewsLike, NewsViews
from serializers import NewsReadSerializer, NewsLikeSerializer, NewsViewSerializer
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.pagination import LimitOffsetPagination
from authentication.tokenauth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from iitbapp.permissions import IsCorrectUserId
from django.shortcuts import get_object_or_404


class NewsPagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 50


class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = News.objects.all().order_by('-id')
    pagination_class = NewsPagination
    serializer_class = NewsReadSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @list_route(methods=['POST'], permission_classes=[IsCorrectUserId])
    def like(self, request):
        serializer = NewsLikeSerializer(data=request.data)
        if serializer.is_valid():
            news_id = serializer.data['news']
            user_id = serializer.data['user']
            self.check_object_permissions(request, user_id)
            news_like, created = NewsLike.objects.get_or_create(news__id=news_id, user__id=user_id,
                                                                defaults={'news_id': news_id, 'user_id': user_id})
            return Response(NewsReadSerializer(news_like.news, context={'request': request}).data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'], permission_classes=[IsCorrectUserId])
    def unlike(self, request):
        serializer = NewsLikeSerializer(data=request.data)
        if serializer.is_valid():
            news_id = serializer.data['news']
            user_id = serializer.data['user']
            self.check_object_permissions(request, user_id)
            NewsLike.objects.all().filter(news=news_id).filter(user=user_id).delete()
            news = get_object_or_404(News, pk=news_id)
            return Response(NewsReadSerializer(news, context={'request': request}).data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'], permission_classes=[IsCorrectUserId])
    def view(self, request):
        serializer = NewsViewSerializer(data=request.data)
        if serializer.is_valid():
            news_id = serializer.data['news']
            user_id = serializer.data['user']
            self.check_object_permissions(request, user_id)
            news_view, created = NewsViews.objects.get_or_create(news__id=news_id, user_id=user_id,
                                                                 defaults={'news_id': news_id, 'user_id': user_id})
            return Response(NewsReadSerializer(news_view.news, context={'request': request}).data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
