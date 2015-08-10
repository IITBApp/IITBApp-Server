from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Case, When, Q, F
from django.db import models

from models import News, NewsLike, NewsViews
from serializers import NewsReadSerializer, NewsLikeSerializer, NewsViewSerializer
from authentication.tokenauth import TokenAuthentication
from core.permissions import IsCorrectUserId


class NewsPagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 50


class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = News.objects.all().order_by('-id')
    pagination_class = NewsPagination
    serializer_class = NewsReadSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        request = self.request
        queryset = News.objects.all().order_by('-id').annotate(
            viewed=Case(
                When(Q(views__user=request.user) & Q(views__news=F('id')), then=True),
                output_field=models.BooleanField(),
                default=False
            ),
            liked=Case(
                When(Q(likes__user=request.user) & Q(likes__news=F('id')), then=True),
                output_field=models.BooleanField(),
                default=False

            )
        )
        return queryset

    @list_route(methods=['POST'], permission_classes=[IsCorrectUserId])
    def like(self, request):
        serializer = NewsLikeSerializer(data=request.data)
        if serializer.is_valid():
            news_id = serializer.data['news']
            user_id = serializer.data['user']
            self.check_object_permissions(request, user_id)
            NewsLike.objects.get_or_create(news_id=news_id, user_id=user_id)
            news = self.get_queryset().filter(id=news_id).first()
            return Response(NewsReadSerializer(news).data)
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
            news = self.get_queryset().filter(id=news_id).first()
            return Response(NewsReadSerializer(news).data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'], permission_classes=[IsCorrectUserId])
    def view(self, request):
        serializer = NewsViewSerializer(data=request.data)
        if serializer.is_valid():
            news_id = serializer.data['news']
            user_id = serializer.data['user']
            self.check_object_permissions(request, user_id)
            news_view, created = NewsViews.objects.get_or_create(news_id=news_id, user_id=user_id)
            news_view.add_view()
            news = self.get_queryset().filter(id=news_id).first()
            return Response(NewsReadSerializer(news).data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
