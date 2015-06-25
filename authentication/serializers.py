__author__ = 'dheerenr'
from rest_framework import serializers
from django.contrib.auth.models import User
from uuid import uuid4
import sys

class UserSerializer(serializers.ModelSerializer):
    roll_number = serializers.CharField(max_length=16, source='username')

    def create(self, validated_data):
        user, created = User.objects.update_or_create(username=validated_data['username'], defaults=validated_data)
        return user

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'roll_number')
