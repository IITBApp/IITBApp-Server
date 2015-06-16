from django.shortcuts import render
from rest_framework import viewsets
from authentication.serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import detail_route, list_route
import sys
from authentication.models import Registration
from django.shortcuts import get_object_or_404

# Create your views here.

class RegistrationViewSet(viewsets.ViewSet):

    

    @list_route(methods=['POST'])
    def add(self, request):

        registration = RegistrationSerializer(data=request.data)

        if registration.is_valid():
            registration.save()
            return Response(registration.data)
        else:
            return Response(registration.errors, status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'])
    def status(self, request):
        registration = RegistrationSerializer(data=request.data)

        if registration.is_valid():
            email = registration.data['email']
            registration = get_object_or_404(Registration, email=email)
            serializer = RegistrationSerializer(registration)
            return Response(serializer.data)
        else:
            return Response(registration.errors, status=status.HTTP_400_BAD_REQUEST)

    @list_route()
    def verify(self, request):
        registration_serialized = RegistrationSerializer(data=request.GET)

        if registration_serialized.is_valid():
            email = registration_serialized.data['email']
            token = request.GET.get('token')
            registration = get_object_or_404(Registration, email=email)
            if registration.token != token:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            else:
                registration.active = True
                registration.save()
                return Response(data='You\'re verified successfully', content_type='text/html')

        else:
            return Response(registration_serialized.errors, status=status.HTTP_400_BAD_REQUEST)

