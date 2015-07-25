from rest_framework.pagination import LimitOffsetPagination
from rest_framework import viewsets
from models import Event, EventLike, EventViews
from rest_framework.decorators import list_route
from serializers import EventReadSerializer, EventLikeSerializer, EventViewSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticated
from iitbapp.permissions import IsCorrectUserId
from authentication.tokenauth import TokenAuthentication
from django.shortcuts import get_object_or_404


class EventPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 50


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all().order_by('-id')
    pagination_class = EventPagination
    serializer_class = EventReadSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @list_route(methods=['POST'], permission_classes=[IsCorrectUserId])
    def like(self, request):
        serializer = EventLikeSerializer(data=request.data)
        if serializer.is_valid():
            event_id = serializer.data['event']
            user_id = serializer.data['user']
            self.check_object_permissions(request, user_id)
            event_like, created = EventLike.objects.get_or_create(event__id=event_id, user__id=user_id,
                                                                  defaults={'event_id': event_id, 'user_id': user_id})
            return Response(EventReadSerializer(event_like.event, context={'request': request}).data)
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
            event = get_object_or_404(Event, pk=event_id)
            return Response(EventReadSerializer(event, context={'request': request}).data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'], permission_classes=[IsCorrectUserId])
    def view(self, request):
        serializer = EventViewSerializer(data=request.data)
        if serializer.is_valid():
            event_id = serializer.data['event']
            user_id = serializer.data['user']
            self.check_object_permissions(request, user_id)
            event_view, created = EventViews.objects.get_or_create(event__id=event_id, user_id=user_id,
                                                                   defaults={'event_id': event_id, 'user_id': user_id})
            return Response(EventReadSerializer(event_view.event, context={'request': request}).data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
