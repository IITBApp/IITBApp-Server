from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework import filters
from rest_framework.exceptions import ValidationError
from django.db.models import Prefetch
from django.contrib.auth.models import User
from pns.models import Device

from .serializers import FeedGenericSerializer, FeedLikeSerializer, FeedViewSerializer, FeedConfigSerializer, \
    FeedEntrySerializer, FeedEntryIdSerializer, FeedCategorySerializer, FeedCategorySubscriptionSerializer
from authentication.tokenauth import TokenAuthentication
from .models import FeedLike, FeedView, FeedConfig, FeedEntry, FeedEntryLike, FeedEntryView
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
    permission_classes = [IsAuthenticated]
    queryset = FeedConfig.objects.all().order_by('-id')
    pagination_class = DefaultLimitOffsetPagination
    filter_backends = [FeedConfigIdFilter]

    def get_queryset(self):
        user = self.request.user
        feed_configs = FeedConfig.objects.all().order_by('-id').prefetch_related(
            Prefetch('categories__subscribers', User.objects.all().filter(pk=user.id))
        )
        return feed_configs

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
        user = self.request.user
        feed_entries = FeedEntryByConfigFilter().filter_queryset(request, self.get_feed_entry_queryset(), self)
        if Device.objects.all().filter(user=user).exists():
            """
            User has registered device in new Device model. Filter entries by subscribed categories now
            Important for maintaining backward compatibility!
            """
            feed_entries = feed_entries.filter(categories__in=user.feed_subscriptions.all())
        feed_entries = self.paginate_queryset(feed_entries)
        serialized_entries = FeedEntrySerializer(feed_entries, many=True).data
        return self.get_paginated_response(serialized_entries)

    @list_route(methods=['POST'])
    def like(self, request):
        serialized = FeedEntryIdSerializer(data=request.DATA)
        if serialized.is_valid():
            entry = serialized.validated_data['entry']
            FeedEntryLike.objects.get_or_create(entry=entry, user=request.user)
            return Response(FeedEntrySerializer(self.get_feed_entry_queryset().get(pk=entry.id)).data)
        else:
            return Response(serialized.errors, status=HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'])
    def view(self, request):
        serialized = FeedEntryIdSerializer(data=request.DATA)
        if serialized.is_valid():
            entry = serialized.validated_data['entry']
            feed_entry_view, created = FeedEntryView.objects.get_or_create(entry=entry, user=request.user)
            feed_entry_view.add_view()
            return Response(FeedEntrySerializer(self.get_feed_entry_queryset().get(id=entry.id)).data)
        else:
            return Response(serialized.errors, status=HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'])
    def unlike(self, request):
        serialized = FeedEntryIdSerializer(data=request.DATA)
        if serialized.is_valid():
            user = request.user
            event = serialized.validated_data['entry']
            FeedEntryLike.objects.all().filter(entry=event).filter(user=user).delete()
            return Response(FeedEntrySerializer(self.get_feed_entry_queryset().get(pk=event.id)).data)
        else:
            return Response(serialized.errors, status=HTTP_400_BAD_REQUEST)

    @list_route(methods=['GET'])
    def subscriptions(self, request):
        queryset = request.user.feed_subscriptions.all()
        categories = self.paginate_queryset(queryset)
        serialized_categories = FeedCategorySerializer(categories, many=True).data
        return self.get_paginated_response(serialized_categories)

    @list_route(methods=['POST'])
    def subscribe(self, request):
        """
        Take a list of category ids, delete all old subscriptions, resubscribe again.
        :param request:
        :return:
        """
        feed_category_subscription_serialiazed = FeedCategorySubscriptionSerializer(data=request.DATA)
        if feed_category_subscription_serialiazed.is_valid():
            categories = feed_category_subscription_serialiazed.validated_data['categories']
            request.user.feed_subscriptions.clear()
            request.user.feed_subscriptions.add(*categories)
            categories = self.paginate_queryset(categories)
            serialized_categories = FeedCategorySerializer(categories, many=True).data
            return self.get_paginated_response(serialized_categories)
        else:
            return Response(feed_category_subscription_serialiazed.errors, status=HTTP_400_BAD_REQUEST)


# TODO: Remove this viewset in future
class FeedViewset(viewsets.GenericViewSet):
    """
    Endpoints for v8 users only
    """
    serializer_class = FeedGenericSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = FeedLike.objects.all()

    @list_route(methods=['POST'])
    def like(self, request):
        feed_like_serializer = FeedLikeSerializer(data=request.DATA)
        if feed_like_serializer.is_valid():
            guid = feed_like_serializer.data['guid']
            user = request.user
            feed_like, created = FeedLike.objects.get_or_create(guid=guid, user=user)
            return Response(FeedLikeSerializer(feed_like).data)
        else:
            return Response(feed_like_serializer.errors, status=HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'])
    def view(self, request):
        feed_view_serializer = FeedViewSerializer(data=request.DATA)
        if feed_view_serializer.is_valid():
            guid = feed_view_serializer.data['guid']
            user = request.user
            feed_view, created = FeedView.objects.get_or_create(guid=guid, user=user)
            feed_view.add_view()
            return Response(FeedViewSerializer(feed_view).data)
        else:
            return Response(feed_view_serializer.errors, status=HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'])
    def unlike(self, request):
        feed_like_serializer = FeedLikeSerializer(data=request.DATA)
        if feed_like_serializer.is_valid():
            guid = feed_like_serializer.data['guid']
            user = request.user
            FeedLike.objects.all().filter(guid=guid).filter(user=user).delete()
            feed = FeedView.objects.get(guid=guid, user=user)
            return Response(FeedLikeSerializer(feed).data)
        else:
            return Response(feed_like_serializer.errors, status=HTTP_400_BAD_REQUEST)
