__author__ = 'dheerenr'

from rest_framework import serializers
from models import Event, EventLike, EventViews
from authentication.serializers import DesignationReadSerializer


class EventWriteSerializer(serializers.ModelSerializer):
    image = serializers.StringRelatedField(many=True, read_only=True)
    likes = serializers.IntegerField(source='likes.count', read_only=True)
    views = serializers.IntegerField(source='views.count', read_only=True)

    class Meta:
        model = Event

class EventReadSerializer(serializers.ModelSerializer):
    likes = serializers.IntegerField(source='likes.count', read_only=True)
    views = serializers.IntegerField(source='views.count', read_only=True)
    posted_by = DesignationReadSerializer(read_only=True)

    class Meta:
        model = Event

class EventLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventLike

class EventViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventViews