from django.contrib import admin
from models import Event, EventImage, EventLike, EventViews
from django.db.models import Prefetch, Sum

class EventAdmin(admin.ModelAdmin):
    # TODO: Add total views if possible in 1 or 2 queries. Adding Sum in queryset gives error
    list_display = ['id', 'title', 'category', 'posted_by', 'total_likes', 'unique_views', 'total_views']

    def get_queryset(self, request):
        queryset = Event.objects.all().prefetch_related(Prefetch('likes', EventLike.objects.all())).prefetch_related(
            Prefetch('views', EventViews.objects.all()))
        return queryset

    def total_likes(self, ins):
        return ins.likes.count()

    def unique_views(self, ins):
        return ins.views.count()

    def total_views(self, ins):
        queryset = ins.views.all()
        queryset = queryset.aggregate(Sum('view_count'))
        return queryset.get('view_count__sum', 0)


class EventImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'event', 'image']


class EventViewAdmin(admin.ModelAdmin):
    list_display = ['id', 'event', 'user']


class EventLikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'event', 'user']


admin.site.register(Event, EventAdmin)
admin.site.register(EventImage, EventImageAdmin)
admin.site.register(EventLike, EventLikeAdmin)
admin.site.register(EventViews, EventViewAdmin)
