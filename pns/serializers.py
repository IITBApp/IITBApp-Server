__author__ = 'dheerendra'

from rest_framework import serializers
from .models import Device


class DeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Device
        read_only_fields = ['user', 'creation_date', 'last_modified', 'is_active']


class DeviceIdSerializer(serializers.Serializer):
    dev_id = serializers.PrimaryKeyRelatedField(queryset=Device.objects.all())
