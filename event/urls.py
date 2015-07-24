__author__ = 'dheerenr'

from django.conf.urls import url, include
from views import EventViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'event', EventViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
]
