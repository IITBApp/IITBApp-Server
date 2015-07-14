from django.shortcuts import render
from rest_framework import viewsets
from serializers import ContactSerializer, ClubSerializer, DepartmentSerializer, EmergencyContactSerializer
from models import Contact, Club, Department, EmergencyContact
from rest_framework.pagination import LimitOffsetPagination

class InformationPaginationClass(LimitOffsetPagination):
    default_limit = 10
    max_limit = 50

class ContactViewset(viewsets.ModelViewSet):

    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    pagination_class = InformationPaginationClass


class ClubViewset(viewsets.ModelViewSet):

    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    pagination_class = InformationPaginationClass


class DepartmentViewset(viewsets.ModelViewSet):

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    pagination_class = InformationPaginationClass


class EmergencyContactViewset(viewsets.ModelViewSet):

    queryset = EmergencyContact.objects.all()
    serializer_class = EmergencyContactSerializer
    pagination_class = InformationPaginationClass
