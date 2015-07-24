__author__ = 'dheerendra'

from rest_framework import serializers
from models import News, NewsImage, NewsLike, NewsViews
from authentication.serializers import UserSerializer, DesignationReadSerializer


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


class NewsLikeSerializer(serializers.ModelSerializer):
    liked = serializers.SerializerMethodField()
    likes = serializers.IntegerField(source='news.likes.count', read_only=True)

    def get_liked(self, obj):
        if self.context.get('liked') is not None:
            return self.context.get('liked')
        return True

    class Meta:
        model = NewsLike


class NewsViewSerializer(serializers.ModelSerializer):
    viewed = serializers.SerializerMethodField()
    views = serializers.IntegerField(source='news.views.count', read_only=True)

    def get_viewed(self, obj):
        if self.context.get('viewed') is not None:
            return self.context.get('viewed')
        return True

    class Meta:
        model = NewsViews
