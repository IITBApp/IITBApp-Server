from django.contrib import admin
from .models import FeedLike, FeedView, FeedConfig, FeedEntry
from django import forms


def check_feed_action(modeladmin, request, queryset):
    for modelinstance in queryset:
        modelinstance.check_feeds(force=True)


check_feed_action.short_description = 'Check for new feeds'


class FeedConfigForm(forms.ModelForm):
    url = forms.URLField(help_text='Enter URL with authentication parameter',
                         widget=forms.TextInput(attrs={'autocomplete': 'off', }))

    def save(self, commit=True):
        feed_config = super(FeedConfigForm, self).save(commit)
        feed_config.url = self.cleaned_data['url']
        feed_config.save()
        return feed_config

    class Meta:
        model = FeedConfig
        fields = ['url', 'check_frequency']


class FeedConfigAdmin(admin.ModelAdmin):
    list_display = ['title', 'link', 'updated', 'last_checked', 'updated', 'check_frequency', 'etag']
    exclude = ['url']

    form = FeedConfigForm

    actions = [check_feed_action]


class FeedEntryAdmin(admin.ModelAdmin):
    list_display = ['id', 'entry_id', 'feed_config', 'title', 'updated', 'published']


class FeedAdmin(admin.ModelAdmin):
    list_display = ['guid', 'user']


admin.site.register(FeedConfig, FeedConfigAdmin)
admin.site.register(FeedEntry, FeedEntryAdmin)
admin.site.register(FeedLike, FeedAdmin)
admin.site.register(FeedView, FeedAdmin)
