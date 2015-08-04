from django.contrib import admin
from .models import FeedLike, FeedView


class FeedAdmin(admin.ModelAdmin):
    list_display = ['guid', 'user']

admin.site.register(FeedLike, FeedAdmin)
admin.site.register(FeedView, FeedAdmin)
