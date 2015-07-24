from django.contrib import admin
from models import Event, EventImage


class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'posted_by']


class EventImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'event', 'image']

admin.site.register(Event, EventAdmin)
admin.site.register(EventImage, EventImageAdmin)
