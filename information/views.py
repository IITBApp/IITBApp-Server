from django.shortcuts import render
from rest_framework import viewsets
from serializers import ContactSerializer, ClubSerializer, DepartmentSerializer, EmergencyContactSerializer
from models import Contact, Club, Department, EmergencyContact
from rest_framework.pagination import LimitOffsetPagination

class InformationPaginationClass(LimitOffsetPagination):
    default_limit = 20
    max_limit = 50

class AbstractInformationViewset(viewsets.ReadOnlyModelViewSet):

    pagination_class = InformationPaginationClass

class ContactViewset(AbstractInformationViewset):

    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class ClubViewset(AbstractInformationViewset):

    queryset = Club.objects.all()
    serializer_class = ClubSerializer


class DepartmentViewset(AbstractInformationViewset):

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class EmergencyContactViewset(AbstractInformationViewset):

    queryset = EmergencyContact.objects.all()
    serializer_class = EmergencyContactSerializer
