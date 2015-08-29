from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticated
from django.db.models import Prefetch

from models import Event, EventLike, EventViews
from serializers import EventReadSerializer, EventIdSerializer
from authentication.tokenauth import TokenAuthentication
from core.pagination import DefaultLimitOffsetPagination


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all().order_by('-id')
    pagination_class = DefaultLimitOffsetPagination
    serializer_class = EventReadSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Event.objects.all().order_by('-id').prefetch_related(
            Prefetch('likes', EventLike.objects.all().filter(user=user), 'liked')
        ).prefetch_related(
            Prefetch('views', EventViews.objects.all().filter(user=user), 'viewed')
        )
        return queryset

    @list_route(methods=['POST'])
    def like(self, request):
        serializer = EventIdSerializer(data=request.data)
        if serializer.is_valid():
            event = serializer.validated_data['event']
            EventLike.objects.get_or_create(event=event, user=request.user)
            event = self.get_queryset().filter(pk=event.id).first()
            return Response(EventReadSerializer(event).data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'])
    def unlike(self, request):
        serializer = EventIdSerializer(data=request.data)
        if serializer.is_valid():
            event = serializer.validated_data['event']
            EventLike.objects.all().filter(event=event).filter(user=request.user).delete()
            event = self.get_queryset().filter(pk=event.id).first()
            return Response(EventReadSerializer(event).data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'])
    def view(self, request):
        serializer = EventIdSerializer(data=request.data)
        if serializer.is_valid():
            event = serializer.validated_data['event']
            event_view, created = EventViews.objects.get_or_create(event=event, user=request.user)
            event_view.add_view()
            event = self.get_queryset().filter(pk=event.id).first()
            return Response(EventReadSerializer(event).data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
