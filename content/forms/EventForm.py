__author__ = 'dheerendra'

from django import forms
from event.models import Event, EventImage
from authentication.models import Designation
from django.utils.translation import gettext as _
from django.utils import timezone
from globals import categories, datetime_input_formats

class EventForm(forms.Form):
    id = forms.IntegerField(required=False)
    title = forms.CharField(max_length=256)
    description = forms.CharField(required=False)
    category = forms.ChoiceField(choices=categories)
    event_time = forms.DateTimeField(input_formats=datetime_input_formats)
    event_place = forms.CharField(max_length=256)
    cancelled = forms.BooleanField()
    event_image = forms.ImageField(required=False)
    designation = forms.IntegerField()

    def __init__(self, user, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        '''
        Validation on the basis of
        1. id should be -1 or None. If anything else is present as id then current user should be owner of that item
        2. designation should belongs to the user who is adding/modifying item
        :return: cleaned_data
        '''
        cleaned_data = super(EventForm, self).clean()
        id = cleaned_data.get('id')
        if id is not None and id != -1:
            event = Event.objects.all().filter(posted_by__user=self.user).filter(id=id)
            if not event.exists():
                raise forms.ValidationError(_('Unauthorised access on event'), code='InvalidAccess')
        designation = Designation.objects.all().filter(user=self.user).filter(pk=cleaned_data['designation'])
        if not designation.exists():
            raise forms.ValidationError(_('The designation provided is invalid'), code='InvalidDesignation')
        if not designation[0].is_active():
            raise forms.ValidationError(_('The designation is outdated. Please use any active designation'),
                                        code='InActiveDesignation')
        event_time = cleaned_data.get('event_time')
        if event_time is not None and event_time < timezone.now():
            raise forms.ValidationError(_('Event time should be in future'), code='InvalidEventDate')
        return cleaned_data

    def save(self):
        id = self.cleaned_data.get('id')
        title = self.cleaned_data.get('title')
        description = self.cleaned_data.get('description')
        category = self.cleaned_data.get('category')
        event_time = self.cleaned_data.get('event_time')
        event_place = self.cleaned_data.get('event_place')
        cancelled = self.cleaned_data.get('cancelled')
        event_image = self.cleaned_data.get('event_image')
        designation = self.cleaned_data.get('designation')
        if id is not None and id != -1:
            event = Event.objects.get(pk=id)
            event.title = title
            event.description = description
            event.category = category
            event.event_time = event_time
            event.event_place = event_place
            event.cancelled = cancelled
            event.posted_by_id = designation
        else:
            event = Event(title=title,
                            description=description,
                            category=category,
                            event_time=event_time,
                            event_place=event_place,
                            cancelled=cancelled,
                            posted_by_id=designation)
        event.save()
        if event_image.image is not None:
            eventImage = EventImage(
                event=event,
                image=event_image
            )
            eventImage.save()
        return event