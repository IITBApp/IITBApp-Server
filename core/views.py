from django.shortcuts import render
from rest_framework import viewsets
from authentication.tokenauth import TokenAuthentication
from iitbapp.permissions import IsCorrectUserId
from rest_framework.permissions import IsAuthenticated
from serializers import BugTrackerSerializer
from models import BugTracker
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

class BugTrackerViewset(viewsets.GenericViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsCorrectUserId]
    serializer_class = BugTrackerSerializer
    queryset = BugTracker.objects.all()

    @list_route(methods=['POST'])
    def add(self, request):
        bug_tracker_serializer = BugTrackerSerializer(data=request.DATA)
        if bug_tracker_serializer.is_valid():
            bug_tracker_serializer.save()
            return Response(bug_tracker_serializer.data)
        else:
            return Response(bug_tracker_serializer.errors, status=HTTP_400_BAD_REQUEST)