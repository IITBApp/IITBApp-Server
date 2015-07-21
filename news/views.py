from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from models import News, NewsImage, NewsLike, NewsViews
from serializers import NewsReadSerializer, NewsWriteSerializer, NewsImageSerializer, NewsLikeSerializer, NewsViewSerializer
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.pagination import LimitOffsetPagination
import globals

class NewsPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 50

class NewsViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = News.objects.all().order_by('-id')
    pagination_class = NewsPagination

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return NewsWriteSerializer
        else:
            return NewsReadSerializer

    @detail_route(methods=['POST'])
    def publish(self, request, pk):
        news = get_object_or_404(News, pk=pk)
        news.published = True
        news.save()
        return Response(NewsReadSerializer(news).data)

    @list_route(methods=['POST'])
    def like(self, request):
        serializer = NewsLikeSerializer(data=request.data)
        if serializer.is_valid():
            news = serializer.data['news']
            user = serializer.data['user']
            news_like, created = NewsLike.objects.get_or_create(news__id=news, user__id=user, defaults={'news_id' : news, 'user_id': user})
            return Response(NewsLikeSerializer(news_like).data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'])
    def unlike(self, request):
        serializer = NewsLikeSerializer(data=request.data)
        if serializer.is_valid():
            news = serializer.data['news']
            user = serializer.data['user']
            NewsLike.objects.all().filter(news=news).filter(user=user).delete()
            return Response({'status': 'deleted'})
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'])
    def view(self, request):
        serializer = NewsViewSerializer(data=request.data)
        if serializer.is_valid():
            news = serializer.data['news']
            user = serializer.data['user']
            news_view, created = NewsViews.objects.get_or_create(news__id=news, user_id=user, defaults={'news_id' : news, 'user_id': user})
            return Response(NewsViewSerializer(news_view).data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @detail_route(methods=['POST', 'PUT'])
    def upload_image(self, request, pk):
        news = get_object_or_404(News, pk=pk)
        image = request.FILES.get('image')
        is_image = globals.verify_image(image)
        if not is_image:
            return Response({'detail': 'Image not found or incorrect file type'}, status=HTTP_400_BAD_REQUEST)
        news_image = NewsImage(news=news, image=image)
        news_image.save()
        return Response(NewsImageSerializer(news_image).data)

    @detail_route(methods=['DELETE'])
    def delete_image(self, request, pk):
        image = get_object_or_404(NewsImage, pk=pk)
        image.delete()
        return Response(NewsImageSerializer(image).data)
