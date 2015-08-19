from rest_framework import viewsets
from .serializers import FeedGenericSerializer, FeedLikeSerializer, FeedViewSerializer, FeedConfigSerializer, \
    FeedEntrySerializer, FeedEntryLikeSerializer, FeedEntryViewSerializer, FeedEntryLike, FeedEntryView
from authentication.tokenauth import TokenAuthentication
from core.permissions import IsCorrectUserId
from rest_framework.permissions import IsAuthenticated
from .models import FeedLike, FeedView, FeedConfig, FeedEntry
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework import filters
from rest_framework.exceptions import ValidationError
from django.db.models import When, Case, Q, F
from django.db import models
from core.pagination import DefaultLimitOffsetPagination


class DummyFeedEntryPagination(DefaultLimitOffsetPagination):

    count = 0
    offset = 0
    limit = 0


class FeedConfigIdFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        ids = request.query_params.get('id', '')
        ids = ids.split(',')
        ids = [id_ for id_ in ids if id_ != '']
        is_valid = all(id_.isdigit() for id_ in ids)
        if not is_valid:
            raise ValidationError('id should be integer of list of integers')
        ids = map(int, ids)
        if ids:
            return queryset.filter(pk__in=ids)
        return queryset


class FeedsViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = FeedConfigSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsCorrectUserId]
    queryset = FeedConfig.objects.all().order_by('-id')
    filter_backends = [FeedConfigIdFilter]
    pagination_class = DummyFeedEntryPagination

    def get_feed_entry_queryset(self):
        user = self.request.user
        feed_entries = FeedEntry.objects.all().annotate(
            viewed=Case(
                When(Q(views__user=user) & Q(views__entry=F('id')), then=True),
                output_field=models.BooleanField(),
                default=False
            ),
            liked=Case(
                When(Q(likes__user=user) & Q(likes__entry=F('id')), then=True),
                output_field=models.BooleanField(),
                default=False
            )
        ).order_by('-updated')
        return feed_entries


    @list_route(methods=['GET'])
    def entries(self, request):
        # TODO: Clean up this hack if you get a chance off your lazy ass

        # TODO: If you're going to change this, then make it flexible. Try to remove the 0:20 limit in better fashion
        feed_configs = self.filter_queryset(self.get_queryset())
        all_feed_entries = []
        for feed_config in feed_configs:
            feed_entries = self.get_feed_entry_queryset().filter(feed_config=feed_config).order_by('-updated')[0:20]
            all_feed_entries.extend(feed_entries)

        serialized_entries = FeedEntrySerializer(all_feed_entries, many=True).data
        response_data = self.get_paginated_response(serialized_entries)
        return response_data

    @list_route(methods=['POST'])
    def like(self, request):
        feed_entry_like_serialized = FeedEntryLikeSerializer(data=request.DATA)
        if feed_entry_like_serialized.is_valid():
            entry_id = feed_entry_like_serialized.data['entry']
            user_id = feed_entry_like_serialized.data['user']
            self.check_object_permissions(request, user_id)
            feed_entry_like, created = FeedEntryLike.objects.get_or_create(entry_id=entry_id, user_id=user_id)
            return Response(FeedEntrySerializer(self.get_feed_entry_queryset().get(id=entry_id)).data)
        else:
            return Response(feed_entry_like_serialized.errors, status=HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'])
    def view(self, request):
        feed_entry_view_serialized = FeedEntryViewSerializer(data=request.DATA)
        if feed_entry_view_serialized.is_valid():
            entry_id = feed_entry_view_serialized.data['entry']
            user_id = feed_entry_view_serialized.data['user']
            self.check_object_permissions(request, user_id)
            feed_entry_view, created = FeedEntryView.objects.get_or_create(entry_id=entry_id, user_id=user_id)
            feed_entry_view.add_view()
            return Response(FeedEntrySerializer(self.get_feed_entry_queryset().get(id=entry_id)).data)
        else:
            return Response(feed_entry_view_serialized.errors, status=HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'])
    def unlike(self, request):
        feed_entry_like_serializer = FeedEntryLikeSerializer(data=request.DATA)
        if feed_entry_like_serializer.is_valid():
            entry_id = feed_entry_like_serializer.data['entry']
            user_id = feed_entry_like_serializer.data['user']
            self.check_object_permissions(request, user_id)
            FeedEntryLike.objects.all().filter(entry_id=entry_id).filter(user_id=user_id).delete()
            feed_entry = FeedEntry.objects.get(pk=entry_id)
            return Response(FeedEntrySerializer(self.get_feed_entry_queryset().get(id=entry_id)).data)
        else:
            return Response(feed_entry_like_serializer.errors, status=HTTP_400_BAD_REQUEST)


# TODO: Remove this viewset in future
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
