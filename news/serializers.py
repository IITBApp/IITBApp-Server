__author__ = 'dheerendra'

from rest_framework import serializers
from models import News, NewsImage, NewsLike, NewsViews
from authentication.serializers import DesignationReadSerializer


class NewsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsImage


class NewsWriteSerializer(serializers.ModelSerializer):
    images = serializers.StringRelatedField(many=True, read_only=True)
    likes = serializers.IntegerField(source='likes.count', read_only=True)
    views = serializers.IntegerField(source='views.count', read_only=True)

    class Meta:
        model = News


class NewsReadSerializer(NewsWriteSerializer):
    posted_by = DesignationReadSerializer(read_only=True)
    liked = serializers.SerializerMethodField()
    viewed = serializers.SerializerMethodField()

    def get_viewed(self, obj):
        if not isinstance(obj, News):
            return False
        request = self.context.get('request')
        if request:
            user = request.user
            return NewsViews.objects.all().filter(news=obj).filter(user=user).exists()
        return False

    def get_liked(self, obj):
        if not isinstance(obj, News):
            return False
        request = self.context.get('request')
        if request:
            user = request.user
            return NewsLike.objects.all().filter(news=obj).filter(user=user).exists()
        return False


class NewsLikeSerializer(serializers.ModelSerializer):
    likes = serializers.IntegerField(source='news.likes.count', read_only=True)

    class Meta:
        model = NewsLike


class NewsViewSerializer(serializers.ModelSerializer):
    views = serializers.IntegerField(source='news.views.count', read_only=True)

    class Meta:
        model = NewsViews
