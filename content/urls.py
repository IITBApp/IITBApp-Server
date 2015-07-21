__author__ = 'dheerendra'

from django.conf.urls import url, include
from views import LoginView, IndexView, LogoutView, AddNoticeView, UserNoticeViewset, UserEventsViewset, AddEventView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('notice', UserNoticeViewset, base_name='notice_url')
router.register('event', UserEventsViewset, base_name='event_url')

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='content_home'),
    url(r'^login/', LoginView.as_view(), name='login_page'),
    url(r'^logout/', LogoutView.as_view(), name='logout_page'),
    url(r'^add_notice/', AddNoticeView.as_view(), name='add_notice'),
    url(r'^add_event/', AddEventView.as_view(), name='add_event'),
    url(r'^api/', include(router.urls)),
]
