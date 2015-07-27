__author__ = 'dheerendra'

from django import forms
from news.models import News, NewsImage
from authentication.models import Designation
from django.utils.translation import gettext as _
from globals import categories
import news.signals as news_signals


class NewsForm(forms.Form):
    id = forms.IntegerField(required=False)
    title = forms.CharField(max_length=256)
    description = forms.CharField(required=False)
    category = forms.ChoiceField(choices=categories)
    news_image = forms.ImageField(required=False)
    designation = forms.IntegerField()

    def __init__(self, user, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        """
        Validation on the basis of
        1. id should be -1 or None. If anything else is present as id then current user should be owner of that item
        2. designation should belongs to the user who is adding/modifying item
        :return: cleaned_data
        """
        cleaned_data = super(NewsForm, self).clean()
        id_ = cleaned_data.get('id')
        if id_ is not None and id_ != -1:
            news = News.objects.all().filter(posted_by__user=self.user).filter(id=id_)
            if not news.exists():
                raise forms.ValidationError(_('Unauthorised access on news'), code='InvalidAccess')
        designation = Designation.objects.all().filter(user=self.user).filter(pk=cleaned_data['designation'])
        if not designation.exists():
            raise forms.ValidationError(_('The designation provided is invalid'), code='InvalidDesignation')
        if not designation[0].is_active():
            raise forms.ValidationError(_('The designation is outdated. Please use any active designation'),
                                        code='InActiveDesignation')
        return cleaned_data

    def save(self):
        id_ = self.cleaned_data.get('id')
        title = self.cleaned_data.get('title')
        description = self.cleaned_data.get('description')
        category = self.cleaned_data.get('category')
        news_image = self.cleaned_data.get('news_image')
        designation = self.cleaned_data.get('designation')
        if id_ is not None and id_ != -1:
            created = False
            news = News.objects.get(pk=id_)
            news.title = title
            news.description = description
            news.category = category
            news.posted_by_id = designation
        else:
            created = True
            news = News(title=title,
                        description=description,
                        category=category,
                        posted_by_id=designation,
                        published=True)
        news.save()
        if news_image is not None and news_image.image is not None:
            '''
            updating old image to just support single image for now. Should be changed in future to support multiple
            images here and at UI side
            '''
            try:
                newsImage = NewsImage.objects.get(news=news)
                newsImage.image = news_image
            except NewsImage.DoesNotExist:
                newsImage = NewsImage(
                    news=news,
                    image=news_image
                )
            newsImage.save()
        news.refresh_from_db()
        news_signals.news_done.send(News, instance=news, created=created)
        return news
