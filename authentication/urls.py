from django.conf.urls import url, include
from rest_framework import routers
from authentication import views

router = routers.DefaultRouter()
router.register(r'registration', views.RegistrationViewSet, base_name='registration_url')

urlpatterns = [
    url(r'^api/', include(router.urls)),
]