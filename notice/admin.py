from django.contrib import admin
from models import Notice

class NoticeAdmin(admin.ModelAdmin):
    list_display = ['title', 'posted_by', 'priority']

admin.site.register(Notice, NoticeAdmin)
