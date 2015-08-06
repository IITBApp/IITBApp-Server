from django.contrib import admin
from models import Event, EventImage, EventLike, EventViews
from django.db.models import Count, Sum


class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'posted_by', 'total_likes', 'unique_views', 'total_views']

    def get_queryset(self, request):
        return Event.objects.all().annotate(total_likes=Count('likes'), unique_views=Count('views'),
                                            total_views=Sum('views__view_count'))

    def total_likes(self, ins):
        return ins.total_likes

    def unique_views(self, ins):
        return ins.unique_views

    def total_views(self, ins):
        return ins.total_views


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
