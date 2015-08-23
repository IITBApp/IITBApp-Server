from django.contrib import admin
from models import BugTracker


class BugTrackerAdmin(admin.ModelAdmin):
    list_display = ['id', 'posted_on', 'phone_model', 'android_version', 'description']


admin.site.register(BugTracker, BugTrackerAdmin)
