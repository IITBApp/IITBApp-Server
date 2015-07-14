__author__ = 'dheerendra'

from django.conf.urls import url, include
from rest_framework import routers
from views import ContactViewset, ClubViewset, DepartmentViewset, EmergencyContactViewset

contactRouter = routers.DefaultRouter()
contactRouter.register(r'contact', ContactViewset)

clubRouter = routers.DefaultRouter()
clubRouter.register(r'club', ClubViewset)

departmentRouter = routers.DefaultRouter()
departmentRouter.register(r'department', DepartmentViewset)

emergencyContactRouter = routers.DefaultRouter()
emergencyContactRouter.register(r'emergency_contact', EmergencyContactViewset)


urlpatterns = [
    url(r'^api/information/', include(contactRouter.urls)),
    url(r'^api/information/', include(clubRouter.urls)),
    url(r'^api/information/', include(departmentRouter.urls)),
    url(r'^api/information/', include(emergencyContactRouter.urls)),
]