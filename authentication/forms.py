__author__ = 'dheerendra'

from django import forms


class LogoutForm(forms.Form):
    logout_all = forms.BooleanField(required=False)