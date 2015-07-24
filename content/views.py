from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django.views.generic import View
from django.contrib.auth import login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from forms.LoginForm import LoginForm
from forms.NoticeForm import NoticeForm
from forms.EventForm import EventForm
from forms.NewsForm import NewsForm
from iitbapp.views import LoginRequiredMixin
from notice.serializers import NoticeReadSerializer
from notice.models import Notice
from event.serializers import EventReadSerializer
from event.models import Event
from news.serializers import NewsReadSerializer
from news.models import News
from authentication.views import authenticate_ldap
from authentication.serializers import UserSerializer


class IndexView(LoginRequiredMixin, View):
    template_name = 'content_home.html'

    def get(self, request):
        designations = request.user.designations.all()
        active_designations = [designation for designation in designations if designation.is_active()]
        return render(request, self.template_name, {'designations': active_designations})


class AddNoticeView(LoginRequiredMixin, APIView):
    renderer_classes = (JSONRenderer,)

    def post(self, request):
        notice_form = NoticeForm(request.user, request.POST)
        if notice_form.is_valid():
            notice = notice_form.save()
            return Response(NoticeReadSerializer(notice).data)
        else:
            return HttpResponseBadRequest(notice_form.errors.as_json(), content_type='application/json')


class AddEventView(LoginRequiredMixin, APIView):
    renderer_classes = (JSONRenderer,)

    def post(self, request):
        event_form = EventForm(request.user, request.POST, request.FILES)
        if event_form.is_valid():
            event = event_form.save()
            return Response(EventReadSerializer(event).data)
        else:
            return HttpResponseBadRequest(event_form.errors.as_json(), content_type='application/json')


class AddNewsView(LoginRequiredMixin, APIView):
    renderer_classes = (JSONRenderer,)

    def post(self, request):
        news_form = NewsForm(request.user, request.POST, request.FILES)
        if news_form.is_valid():
            news = news_form.save()
            return Response(NewsReadSerializer(news).data)
        else:
            return HttpResponseBadRequest(news_form.errors.as_json(), content_type='application/json')


class LoginView(View):
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

            response_data = authenticate_ldap(username, password)

            user = None

            if not response_data['error']:
                user_serialized = UserSerializer(data=response_data)
                if user_serialized.is_valid():
                    user = user_serialized.save()
                    user.backend = "django.contrib.auth.backends.ModelBackend"

                    #            user = authenticate(username=username, password=password)
            if user is not None and user.is_authenticated():
                designations = user.designations.all()
                have_active_designation = any([designation.is_active() for designation in designations])
                if have_active_designation:
                    login(request, user)
                    next_ = request.GET.get('next')
                    if next_ is not None:
                        return redirect(next_)
                else:
                    form.add_error(None,
                                   "You don't have content creation access. "
                                   "If you wish to get permissions, please contact Aman Gour")
                    return render(request, self.template_name, {'form': form})
                return redirect('content_home')
            else:
                form.add_error(None, "Unable to authenticate. Please check username/password")
        return render(request, self.template_name, {'form': form})


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('login_page')


class ReadOnlyModelViewsetPaginator(LimitOffsetPagination):
    default_limit = 10
    max_limit = 50


class UserNoticeViewset(viewsets.ReadOnlyModelViewSet):
    pagination_class = ReadOnlyModelViewsetPaginator
    serializer_class = NoticeReadSerializer
    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'notice/notice_list.html'

    def get_queryset(self):
        return Notice.objects.all().filter(posted_by__user=self.request.user)


class UserEventsViewset(viewsets.ReadOnlyModelViewSet):
    pagination_class = ReadOnlyModelViewsetPaginator
    serializer_class = EventReadSerializer
    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'event/event_list.html'

    def get_queryset(self):
        return Event.objects.all().filter(posted_by__user=self.request.user)


class UserNewsViewset(viewsets.ReadOnlyModelViewSet):
    pagination_class = ReadOnlyModelViewsetPaginator
    serializer_class = NewsReadSerializer
    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'news/news_list.html'

    def get_queryset(self):
        return News.objects.all().filter(posted_by__user=self.request.user)
