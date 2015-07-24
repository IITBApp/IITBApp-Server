__author__ = 'dheerendra'

from rest_framework import serializers
from models import Notice
from authentication.serializers import DesignationReadSerializer


class NoticeWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notice


class NoticeReadSerializer(NoticeWriteSerializer):
    posted_by = DesignationReadSerializer(read_only=True)
