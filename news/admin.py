from django.contrib import admin
from models import News, NewsImage


class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'posted_by', 'time']


class NewsImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'news', 'image']


admin.site.register(News, NewsAdmin)
admin.site.register(NewsImage, NewsImageAdmin)
