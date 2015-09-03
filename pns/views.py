from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from authentication.tokenauth import TokenAuthentication
from .models import Device
from .serializers import DeviceSerializer
from core.permissions import UserIsForeignKey
from .forms import DeviceRegistrationForm, DeviceDeregistrationForm


class PNSViewset(viewsets.GenericViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    @list_route(methods=['POST'])
    def register(self, request):
        registration_form = DeviceRegistrationForm(data=request.DATA)
        if registration_form.is_valid():
            dev_id = registration_form.cleaned_data['dev_id']
            reg_id = registration_form.cleaned_data['reg_id']
            device, created = Device.objects.update_or_create(dev_id=dev_id, user=request.user,
                                                              defaults={'reg_id': reg_id, 'is_active': True})
            return Response(self.serializer_class(device).data)
        else:
            return Response(registration_form.errors, status=HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'], permission_classes=[IsAuthenticated, UserIsForeignKey])
    def deregister(self, request):
        deregistration_form = DeviceDeregistrationForm(data=request.DATA)
        if deregistration_form.is_valid():
            dev_id = deregistration_form.cleaned_data['dev_id']
            device = self.queryset.filter(dev_id=dev_id).first()
            self.check_object_permissions(request, device)
            device.is_active = False
            device.save()
            return Response(self.serializer_class(device).data)
        else:
            return Response(deregistration_form.errors, status=HTTP_400_BAD_REQUEST)
