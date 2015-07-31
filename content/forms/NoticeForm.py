__author__ = 'dheerendra'

from django import forms
from django.utils.translation import gettext as _
from django.utils import timezone

from core.globals import notice_priority, datetime_input_formats
from notice.models import Notice
from authentication.models import Designation
import notice.signals as notice_signals


class NoticeForm(forms.Form):
    id = forms.IntegerField(required=False)
    title = forms.CharField(max_length=256)
    description = forms.CharField(required=False)
    priority = forms.ChoiceField(choices=notice_priority)
    expiration_date = forms.DateTimeField(required=False, input_formats=datetime_input_formats)
    designation = forms.IntegerField()
    notify_users = forms.BooleanField(required=False)

    def __init__(self, user, *args, **kwargs):
        super(NoticeForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        """
        Validation on the basis of
        1. id should be -1 or None. If anything else is present as id then current user should be owner of that item
        2. designation should belongs to the user who is adding/modifying item
        :return: cleaned_data
        """
        cleaned_data = super(NoticeForm, self).clean()
        id_ = cleaned_data.get('id')
        if id_ is not None and id_ != -1:
            notice = Notice.objects.all().filter(posted_by__user=self.user).filter(id=id_)
            if not notice.exists():
                raise forms.ValidationError(_('Unauthorised access on notice'), code='InvalidAccess')
        designation = Designation.objects.all().filter(user=self.user).filter(pk=cleaned_data['designation'])
        if not designation.exists():
            raise forms.ValidationError(_('The designation provided is invalid'), code='InvalidDesignation')
        if not designation[0].is_active():
            raise forms.ValidationError(_('The designation is outdated. Please use any active designation'),
                                        code='InActiveDesignation')
        expiration_date = cleaned_data.get('expiration_date')
        if expiration_date is not None and expiration_date < timezone.now():
            raise forms.ValidationError(_('Expiration date should be in future'), code='InvalidExpirationDate')
        return cleaned_data

    def save(self):
        id_ = self.cleaned_data.get('id')
        title = self.cleaned_data.get('title')
        description = self.cleaned_data.get('description')
        priority = self.cleaned_data.get('priority')
        expiration_date = self.cleaned_data.get('expiration_date')
        designation = self.cleaned_data.get('designation')
        notify_users = self.cleaned_data.get('notify_users')
        if id_ is not None and id_ != -1:
            notice = Notice.objects.get(pk=id_)
            notice.title = title
            notice.description = description
            notice.priority = priority
            notice.expiration_date = expiration_date
            notice.posted_by_id = designation
            created = False
        else:
            notice = Notice(title=title,
                            description=description,
                            priority=priority,
                            expiration_date=expiration_date,
                            posted_by_id=designation)
            notify_users = True
            created = True
        notice.save()
        if notify_users:
            notice.refresh_from_db()
            notice_signals.notice_done.send(Notice, instance=notice, created=created)
        return notice
