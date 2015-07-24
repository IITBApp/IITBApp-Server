__author__ = 'dheerendra'

from rest_framework import serializers
from models import Contact, Club, Department, EmergencyContact


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact


class ClubSerializer(serializers.ModelSerializer):

    class Meta:
        model = Club


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department


class EmergencyContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmergencyContact
