__author__ = 'dheerendra'

from django.conf.urls import url, include
from views import LoginView, IndexView, LogoutView, AddNoticeView, UserNoticeViewset, UserEventsViewset, AddEventView, \
    AddNewsView, UserNewsViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('notice', UserNoticeViewset, base_name='content_notice')
router.register('event', UserEventsViewset, base_name='content_event')
router.register('news', UserNewsViewset, base_name='content_news')

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='content_home'),
    url(r'^login/', LoginView.as_view(), name='login_page'),
    url(r'^logout/', LogoutView.as_view(), name='logout_page'),
    url(r'^add_notice/', AddNoticeView.as_view(), name='add_content_notice'),
    url(r'^add_event/', AddEventView.as_view(), name='add_content_event'),
    url(r'^add_news/', AddNewsView.as_view(), name='add_content_news'),
    url(r'^api/', include(router.urls)),
]
