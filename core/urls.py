__author__ = 'dheerendra'

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from views import BugTrackerViewset

router = DefaultRouter()
router.register('bug', BugTrackerViewset)


urlpatterns = [
    url('^api/', include(router.urls)),
]