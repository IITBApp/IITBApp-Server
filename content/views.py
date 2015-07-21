from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest

from django.views.generic import View
from forms.LoginForm import LoginForm
from forms.NoticeForm import NoticeForm
from forms.EventForm import EventForm
from forms.NewsForm import NewsForm
from django.contrib.auth import authenticate, login, logout
from iitbapp.views import StrongholdPublicMixin
from rest_framework.response import Response
from notice.serializers import NoticeReadSerializer
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from notice.models import Notice
from event.serializers import EventReadSerializer
from event.models import Event
from news.serializers import NewsReadSerializer
from news.models import News

class IndexView(View):

    template_name = 'content_home.html'

    def get(self, request):
        designations = request.user.designations.all()
        active_designations = [designation for designation in designations if designation.is_active()]
        return render(request, self.template_name, {'designations': active_designations})

class AddNoticeView(APIView):

    renderer_classes = (JSONRenderer, )

    def post(self, request):
        noticeForm = NoticeForm(request.user, request.POST)
        if noticeForm.is_valid():
            notice = noticeForm.save()
            return Response(NoticeReadSerializer(notice).data)
        else:
            return HttpResponseBadRequest(noticeForm.errors.as_json(), content_type='application/json')

class AddEventView(APIView):

    renderer_classes = (JSONRenderer, )

    def post(self, request):
        eventForm = EventForm(request.user, request.POST, request.FILES)
        if eventForm.is_valid():
            event = eventForm.save()
            return Response(EventReadSerializer(event).data)
        else:
            return HttpResponseBadRequest(eventForm.errors.as_json(), content_type='application/json')

class AddNewsView(APIView):

    renderer_classes = (JSONRenderer, )

    def post(self, request):
        newsForm = NewsForm(request.user, request.POST, request.FILES)
        if newsForm.is_valid():
            news = newsForm.save()
            return Response(NewsReadSerializer(news).data)
        else:
            return HttpResponseBadRequest(newsForm.errors.as_json(), content_type='application/json')


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


class ReadOnlyModelViewsetPaginator(LimitOffsetPagination):

    default_limit = 10
    max_limit = 50

class UserNoticeViewset(viewsets.ReadOnlyModelViewSet):

    pagination_class = ReadOnlyModelViewsetPaginator
    serializer_class = NoticeReadSerializer
    renderer_classes = (TemplateHTMLRenderer, )
    template_name = 'notice/notice_list.html'

    def get_queryset(self):
        return Notice.objects.all().filter(posted_by__user=self.request.user)

class UserEventsViewset(viewsets.ReadOnlyModelViewSet):

    pagination_class = ReadOnlyModelViewsetPaginator
    serializer_class = EventReadSerializer
    renderer_classes = (TemplateHTMLRenderer, )
    template_name = 'event/event_list.html'

    def get_queryset(self):
        return Event.objects.all().filter(posted_by__user=self.request.user)

class UserNewsViewset(viewsets.ReadOnlyModelViewSet):

    pagination_class = ReadOnlyModelViewsetPaginator
    serializer_class = NewsReadSerializer
    renderer_classes = (TemplateHTMLRenderer, )
    template_name = 'news/news_list.html'

    def get_queryset(self):
        return News.objects.all().filter(posted_by__user=self.request.user)

