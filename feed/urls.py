__author__ = 'dheerenr'

from django.conf.urls import url, include
from views import FeedViewset, FeedsViewset
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'feed', FeedViewset)
router.register(r'feeds', FeedsViewset)

urlpatterns = [
    url(r'^api/', include(router.urls)),
]
