__author__ = 'dheerenr'

from django.conf.urls import url, include
from views import FeedViewset
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'feed', FeedViewset)

urlpatterns = [
    url(r'^api/', include(router.urls)),
]
