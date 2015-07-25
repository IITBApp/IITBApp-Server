from django.contrib import admin
from models import Event, EventImage, EventLike, EventViews


class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'posted_by']


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
