from django.shortcuts import render, redirect

from django.views.generic import View
from forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from stronghold.decorators import public
from iitbapp.views import StrongholdPublicMixin

class IndexView(View):

    template_name = 'content_home.html'

    def get(self, request):
        designations = request.user.designations.all()
        active_designations = []
        #TODO: filter out active designations
        return render(request, self.template_name, {'designations': designations})

class AddPostView(View):

    def post(self, request):
        pass

class LoginView(StrongholdPublicMixin, View):

    template_name = 'login.html'

    def get(self, request):
        if request.user.is_authenticated():
            return redirect('content_home')
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user is not None and user.is_authenticated():
                designations = user.designations.all()
                have_active_designation = any([designation.is_active() for designation in designations])
                if have_active_designation:
                    login(request, user)
                    next = request.GET.get('next')
                    if next is not None:
                        return redirect(next)
                else:
                    form.add_error(None, "Unable to authenticate. No active PoR found")
                    return render(request, self.template_name, {'form': form})
                return redirect('content_home')
            else:
                form.add_error(None, "Unable to authenticate. Please check username/password")
        return render(request, self.template_name, {'form': form})

class LogoutView(StrongholdPublicMixin, View):

    def get(self, request):
        logout(request)
        return redirect('login_page')