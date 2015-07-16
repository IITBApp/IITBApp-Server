__author__ = 'dheerendra'

from django.conf.urls import url
from views import LoginView, IndexView, LogoutView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='content_home'),
    url(r'^login/', LoginView.as_view(), name='login_page'),
    url(r'^logout/', LogoutView.as_view(), name='logout_page'),
]
