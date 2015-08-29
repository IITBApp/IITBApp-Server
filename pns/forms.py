__author__ = 'dheerendra'

from django import forms
from .models import Device


class DeviceRegistrationForm(forms.Form):
    dev_id = forms.CharField()
    reg_id = forms.CharField()


class DeviceDeregistrationForm(forms.Form):
    dev_id = forms.CharField()