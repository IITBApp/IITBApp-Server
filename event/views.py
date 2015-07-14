from django.shortcuts import get_object_or_404

# Create your views here.
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import viewsets
from models import Event, EventLike, EventViews, EventImage
from rest_framework.decorators import list_route, detail_route
from serializers import EventReadSerializer, EventWriteSerializer, EventLikeSerializer, EventViewSerializer, EventImageSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
import globals

class EventPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 50

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    pagination_class = EventPagination

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return EventWriteSerializer
        else:
            return EventReadSerializer

    @list_route(methods=['POST'])
    def like(self, request):
        serializer = EventLikeSerializer(data=request.data)
        if serializer.is_valid():
            event = serializer.data['event']
            user = serializer.data['user']
            event_like, created = EventLike.objects.get_or_create(event__id=event, user__id=user, defaults={'event_id' : event, 'user_id': user})
            return Response(EventLikeSerializer(event_like).data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'])
    def unlike(self, request):
        serializer = EventLikeSerializer(data=request.data)
        if serializer.is_valid():
            event = serializer.data['event']
            user = serializer.data['user']
            EventLike.objects.all().filter(event=event).filter(user=user).delete()
            return Response({'status': 'deleted'})
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'])
    def view(self, request):
        serializer = EventViewSerializer(data=request.data)
        if serializer.is_valid():
            event = serializer.data['event']
            user = serializer.data['user']
            event_view, created = EventViews.objects.get_or_create(event__id=event, user_id=user, defaults={'event_id' : event, 'user_id': user})
            return Response(EventViewSerializer(event_view).data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @detail_route(methods=['POST'])
    def cancel(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        event.cancelled = True
        event.save()
        return Response(EventReadSerializer(event).data)

    @detail_route(methods=['POST', 'PUT'])
    def upload_image(self, request, pk):
        news = get_object_or_404(Event, pk=pk)
        image = request.FILES.get('image')
        is_image = globals.verify_image(image)
        if not is_image:
            return Response({'detail': 'Image not found or incorrect file type'}, status=HTTP_400_BAD_REQUEST)
        news_image = EventImage(news=news, image=image)
        news_image.save()
        return Response(EventImageSerializer(news_image).data)

    @detail_route(methods=['DELETE'])
    def delete_image(self, request, pk):
        image = get_object_or_404(EventImage, pk=pk)
        image.delete()
        return Response(EventImageSerializer(image).data)
