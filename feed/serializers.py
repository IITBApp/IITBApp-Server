__author__ = 'dheerendra'

from rest_framework import serializers
from .models import FeedLike, FeedView, FeedConfig, FeedEntry, FeedEntryLike, FeedEntryView


class FeedEntrySerializer(serializers.ModelSerializer):
    liked = serializers.SerializerMethodField()
    viewed = serializers.SerializerMethodField()
    likes = serializers.IntegerField(source='likes.count')
    views = serializers.IntegerField(source='views.count')

    def get_liked(self, obj):
        if hasattr(obj, 'liked'):
            return obj.liked
        return False

    def get_viewed(self, obj):
        if hasattr(obj, 'viewed'):
            return obj.viewed
        return False

    class Meta:
        model = FeedEntry
        fields = ['id', 'feed_config', 'title', 'link', 'updated', 'content', 'author', 'liked', 'viewed', 'likes', 'views']


class FeedConfigSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeedConfig
        fields = ['id', 'title', 'link', 'updated']


class FeedEntryLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeedEntryLike


class FeedEntryViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeedEntryView


#TODO: Remove Generic Serializer and FeedLike Serializer
def parse_data(obj):
    return obj.guid, obj.user


class FeedGenericSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    views = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()
    viewed = serializers.SerializerMethodField()

    def get_liked(self, obj):
        try:
            guid, user = parse_data(obj)
            return FeedLike.objects.all().filter(guid=guid).filter(user=user).exists()
        except:
            return False

    def get_viewed(self, obj):
        try:
            guid, user = parse_data(obj)
            return FeedView.objects.all().filter(guid=guid).filter(user=user).exists()
        except:
            return False

    def get_likes(self, obj):
        try:
            guid, user = parse_data(obj)
            return FeedLike.objects.all().filter(guid=guid).count()
        except:
            return 0

    def get_views(self, obj):
        try:
            guid, user = parse_data(obj)
            return FeedView.objects.all().filter(guid=guid).count()
        except:
            return 0


class FeedLikeSerializer(FeedGenericSerializer):

    class Meta:
        model = FeedLike


class FeedViewSerializer(FeedGenericSerializer):

    class Meta:
        model = FeedView
        exclude = ['view_count']