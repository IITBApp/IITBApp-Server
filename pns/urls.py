__author__ = 'dheerendra'

from rest_framework.routers import DefaultRouter
from .views import PNSViewset
from django.conf.urls import url, include

router = DefaultRouter()
router.register('pns', PNSViewset)

urlpatterns = [
    url(r'^api/', include(router.urls)),
]