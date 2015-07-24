__author__ = 'dheerenr'

from django.conf.urls import url, include
from rest_framework import routers
from views import UserViewset

router = routers.DefaultRouter()
router.register(r'users', UserViewset)

urlpatterns = [
    url(r'^api/', include(router.urls)),
]
