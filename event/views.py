from rest_framework.pagination import LimitOffsetPagination
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from models import Event, EventLike, EventViews
from serializers import EventReadSerializer, EventLikeSerializer, EventViewSerializer
from core.permissions import IsCorrectUserId
from authentication.tokenauth import TokenAuthentication
from django.db.models import Count, Case, When, Q, F
from django.db import models


class EventPagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 50


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all().order_by('-id')
    pagination_class = EventPagination
    serializer_class = EventReadSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        request = self.request
        queryset = Event.objects.all().order_by('-id').annotate(
            viewed = Case(
                When(Q(views__user=request.user) & Q(views__event=F('id')), then=True),
                output_field=models.BooleanField(),
                default=False
            ),
            liked= Case(
                When(Q(likes__user=request.user) & Q(likes__event=F('id')), then=True),
                output_field=models.BooleanField(),
                default=False

            )
        )
        return queryset

    @list_route(methods=['POST'], permission_classes=[IsCorrectUserId])
    def like(self, request):
        serializer = EventLikeSerializer(data=request.data)
        if serializer.is_valid():
            event_id = serializer.data['event']
            user_id = serializer.data['user']
            self.check_object_permissions(request, user_id)
            EventLike.objects.get_or_create(event_id=event_id, user_id=user_id)
            event = self.get_queryset().filter(id=event_id).first()
            return Response(EventReadSerializer(event).data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'], permission_classes=[IsCorrectUserId])
    def unlike(self, request):
        serializer = EventLikeSerializer(data=request.data)
        if serializer.is_valid():
            event_id = serializer.data['event']
            user_id = serializer.data['user']
            self.check_object_permissions(request, user_id)
            EventLike.objects.all().filter(event=event_id).filter(user=user_id).delete()
            event = self.get_queryset().filter(id=event_id).first()
            return Response(EventReadSerializer(event).data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'], permission_classes=[IsCorrectUserId])
    def view(self, request):
        serializer = EventViewSerializer(data=request.data)
        if serializer.is_valid():
            event_id = serializer.data['event']
            user_id = serializer.data['user']
            self.check_object_permissions(request, user_id)
            event_view, created = EventViews.objects.get_or_create(event_id=event_id, user_id=user_id)
            event_view.add_view()
            event = self.get_queryset().filter(id=event_id).first()
            return Response(EventReadSerializer(event).data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
