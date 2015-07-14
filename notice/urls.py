__author__ = 'dheerendra'

from django.conf.urls import url, include
from rest_framework import routers
from views import NoticeViewset

router = routers.DefaultRouter()
router.register(r'notice', NoticeViewset)

urlpatterns = [
    url(r'^api/', include(router.urls)),
]