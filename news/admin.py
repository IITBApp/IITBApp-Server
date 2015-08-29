from django.contrib import admin
from models import News, NewsImage, NewsLike, NewsViews
from django.db.models import Prefetch


class NewsAdmin(admin.ModelAdmin):
    #TODO: Add total views just like event
    list_display = ['id', 'title', 'category', 'posted_by', 'time', 'total_likes', 'unique_views']

    def get_queryset(self, request):
        queryset = News.objects.all().prefetch_related(
            Prefetch('likes', NewsLike.objects.all())
        ).prefetch_related(
            Prefetch('views', NewsViews.objects.all())
        )
        return queryset

    def total_likes(self, ins):
        return ins.likes.count()

    def unique_views(self, ins):
        return ins.views.count()


class NewsImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'news', 'image']


admin.site.register(News, NewsAdmin)
admin.site.register(NewsImage, NewsImageAdmin)
