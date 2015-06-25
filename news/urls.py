__author__ = 'dheerenr'

from django.conf.urls import url, include
from views import NewsViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'news', NewsViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
]
