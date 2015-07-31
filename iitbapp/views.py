__author__ = 'dheerendra'

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings
import os
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test


class LoginRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


def index(request):
    return render(request, 'iitbapp/index.html', {})


def about(request):
    return render(request, 'iitbapp/about.html', {})


@user_passes_test(lambda user: user.is_staff)
def logs(request):
    response = HttpResponse(content_type="text/plain")

    file_ = os.path.join(settings.BASE_DIR, 'logs/application.log')

    with open(file_) as f:
        content = f.read()
        response.write(content)
    return response
