__author__ = 'dheerenr'

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
    class Meta:
        model = NewsLike

class NewsViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsViews