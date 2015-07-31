__author__ = 'dheerendra'

from django import forms


class LogoutForm(forms.Form):
    user = forms.IntegerField()
    logout_all = forms.BooleanField(required=False)