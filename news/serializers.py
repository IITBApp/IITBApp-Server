__author__ = 'dheerendra'

from rest_framework import serializers
from models import News, NewsImage
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
        if hasattr(obj, 'viewed'):
            return len(obj.viewed) > 0
        else:
            return False

    def get_liked(self, obj):
        if hasattr(obj, 'liked'):
            return len(obj.liked) > 0
        else:
            return False


class NewsIdSerializer(serializers.Serializer):
    news = serializers.PrimaryKeyRelatedField(queryset=News.objects.all())
