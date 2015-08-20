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
from django.db.models import Prefetch
from core.pagination import DefaultLimitOffsetPagination


def get_ids(request):
    ids = request.query_params.get('id', '')
    ids = ids.split(',')
    ids = [id_ for id_ in ids if id_ != '']
    is_valid = all(id_.isdigit() for id_ in ids)
    if not is_valid:
        raise ValidationError('id should be a list of integers')
    ids = map(int, ids)
    return ids


class FeedConfigIdFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        ids = get_ids(request)
        if ids:
            return queryset.filter(pk__in=ids)
        return queryset


class FeedEntryByConfigFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        ids = get_ids(request)
        if ids:
            return queryset.filter(feed_config_id__in=ids)
        return queryset


class FeedsViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = FeedConfigSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsCorrectUserId]
    queryset = FeedConfig.objects.all().order_by('-id')
    pagination_class = DefaultLimitOffsetPagination
    filter_backends = [FeedConfigIdFilter]

    def get_feed_entry_queryset(self):
        user = self.request.user
        feed_entries = FeedEntry.objects.all().order_by('-updated').prefetch_related(
            Prefetch('likes', FeedEntryLike.objects.all().filter(user=user), 'liked')
        ).prefetch_related(
            Prefetch('views', FeedEntryView.objects.all().filter(user=user), 'viewed')
        )
        return feed_entries

    @list_route(methods=['GET'])
    def entries(self, request):
        feed_entries = FeedEntryByConfigFilter().filter_queryset(request, self.get_feed_entry_queryset(), self)
        feed_entries = self.paginate_queryset(feed_entries)
        serialized_entries = FeedEntrySerializer(feed_entries, many=True).data
        return self.get_paginated_response(serialized_entries)

    @list_route(methods=['POST'])
    def like(self, request):
        feed_entry_like_serialized = FeedEntryLikeSerializer(data=request.DATA)
        if feed_entry_like_serialized.is_valid():
            entry_id = feed_entry_like_serialized.data['entry']
            user_id = feed_entry_like_serialized.data['user']
            self.check_object_permissions(request, user_id)
            FeedEntryLike.objects.get_or_create(entry_id=entry_id, user_id=user_id)
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
            FeedEntry.objects.get(pk=entry_id)
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
