from django.contrib import admin
from models import News, NewsImage, NewsLike, NewsViews
from django.db.models import Count

class NewsAdmin(admin.ModelAdmin):
    #TODO: Add total views just like event
    list_display = ['id', 'title', 'category', 'posted_by', 'time', 'total_likes', 'unique_views']

    def get_queryset(self, request):
        queryset = News.objects.all().annotate(total_likes=Count('likes', distinct=True),
                                                unique_views=Count('views', distinct=True))
        return queryset

    def total_likes(self, ins):
        return ins.total_likes

    def unique_views(self, ins):
        return ins.unique_views


class NewsImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'news', 'image']


class NewsLikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'news', 'user']


class NewsViewAdmin(admin.ModelAdmin):
    list_display = ['id', 'news', 'user']

admin.site.register(News, NewsAdmin)
admin.site.register(NewsImage, NewsImageAdmin)
admin.site.register(NewsLike, NewsLikeAdmin)
admin.site.register(NewsViews, NewsViewAdmin)
