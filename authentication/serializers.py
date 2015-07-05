__author__ = 'dheerenr'
from rest_framework import serializers
from django.contrib.auth.models import User
from models import Designation
from uuid import uuid4
from datetime import datetime
import sys

class UserSerializer(serializers.ModelSerializer):
    employeeNumber = serializers.CharField(max_length=16, source='username')

    def create(self, validated_data):
        user, created = User.objects.update_or_create(username=validated_data['username'], defaults=validated_data)
        return user

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'employeeNumber')


class DesignationReadSerializer(serializers.ModelSerializer):
    post = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    def get_email(self, obj):
        return obj.user.email

    def get_name(self, obj):
        return obj.user.first_name + " " + obj.user.last_name

    def get_post(self, obj):
        post = obj.post
        curr_date = datetime.now().date()
        if (curr_date > obj.end_date):
            post = "Ex. " + post
        return post

    class Meta:
        model = Designation
        fields = ['name', 'email', 'post']

