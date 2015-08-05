from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .serializers import FeedGenericSerializer, FeedLikeSerializer, FeedViewSerializer
from authentication.tokenauth import TokenAuthentication
from core.permissions import IsCorrectUserId
from rest_framework.permissions import IsAuthenticated
from .models import FeedLike, FeedView
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

class FeedViewset(viewsets.GenericViewSet):

    serializer_class = FeedGenericSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCorrectUserId, IsAuthenticated]
    queryset = FeedLike.objects.all()

    @list_route(methods=['POST'])
    def like(self, request):
        feed_like_serializer = FeedLikeSerializer(data=request.DATA)
        if feed_like_serializer.is_valid():
            guid = feed_like_serializer.data['guid']
            user = feed_like_serializer.data['user']
            self.check_object_permissions(request, user)
            feed_like, created = FeedLike.objects.get_or_create(guid=guid, user_id=user)
            return Response(FeedLikeSerializer(feed_like).data)
        else:
            return Response(feed_like_serializer.errors, status=HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'])
    def view(self, request):
        feed_view_serializer = FeedViewSerializer(data=request.DATA)
        if feed_view_serializer.is_valid():
            guid = feed_view_serializer.data['guid']
            user = feed_view_serializer.data['user']
            self.check_object_permissions(request, user)
            feed_view, created = FeedView.objects.get_or_create(guid=guid, user_id=user)
            feed_view.add_view()
            return Response(FeedViewSerializer(feed_view).data)
        else:
            return Response(feed_view_serializer.errors, status=HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'])
    def unlike(self, request):
        feed_like_serializer = FeedLikeSerializer(data=request.DATA)
        if feed_like_serializer.is_valid():
            guid = feed_like_serializer.data['guid']
            user = feed_like_serializer.data['user']
            self.check_object_permissions(request, user)
            FeedLike.objects.all().filter(guid=guid).filter(user=user).delete()
            feed = FeedView.objects.get(guid=guid, user=user)
            return Response(FeedLikeSerializer(feed).data)
        else:
            return Response(feed_like_serializer.errors, status=HTTP_400_BAD_REQUEST)


