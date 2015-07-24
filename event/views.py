from rest_framework.pagination import LimitOffsetPagination
from rest_framework import viewsets
from models import Event, EventLike, EventViews
from rest_framework.decorators import list_route
from serializers import EventReadSerializer, EventLikeSerializer, EventViewSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST


class EventPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 50


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all().order_by('-id')
    pagination_class = EventPagination
    serializer_class = EventReadSerializer

    @list_route(methods=['POST'])
    def like(self, request):
        serializer = EventLikeSerializer(data=request.data)
        if serializer.is_valid():
            event = serializer.data['event']
            user = serializer.data['user']
            event_like, created = EventLike.objects.get_or_create(event__id=event, user__id=user,
                                                                  defaults={'event_id': event, 'user_id': user})
            return Response(EventLikeSerializer(event_like, context={'liked': created}).data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'])
    def unlike(self, request):
        serializer = EventLikeSerializer(data=request.data)
        if serializer.is_valid():
            event = serializer.data['event']
            user = serializer.data['user']
            EventLike.objects.all().filter(event=event).filter(user=user).delete()
            likes = EventLike.objects.all().filter(news=event).count()
            return Response({'status': 'deleted', 'likes': likes})
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'])
    def view(self, request):
        serializer = EventViewSerializer(data=request.data)
        if serializer.is_valid():
            event = serializer.data['event']
            user = serializer.data['user']
            event_view, created = EventViews.objects.get_or_create(event__id=event, user_id=user,
                                                                   defaults={'event_id': event, 'user_id': user})
            return Response(EventViewSerializer(event_view, context={'viewed': created}).data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
