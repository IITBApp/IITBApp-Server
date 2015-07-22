"""iitbapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from authentication import urls as authentication_urls
from news import urls as news_urls
from event import urls as event_urls
from notice import urls as notice_urls
from information import urls as information_urls
from content import urls as content_urls
import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^public/', include(information_urls)),
    url(r'^content/', include(content_urls)),
    url(r'^logs/', views.logs),
    url(r'', include(authentication_urls)),
    url(r'', include(news_urls)),
    url(r'', include(event_urls)),
    url(r'', include(notice_urls)),
    url(r'', include('gcm.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
    )