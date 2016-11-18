from bootstrap3_datetime.widgets import DateTimePicker
from crispy_forms.helper import FormHelper
from django import forms
from django.conf import settings

from .models import DirectoryEntry, OpeningHour


class DirectoryEntryForm(forms.ModelForm):
    class Meta(object):
        model = DirectoryEntry
        fields = ['description', 'contact_address', 'phone', 'website_url', 'facebook_url', 'twitter_url', 'place']

    def __init__(self, *args, **kwargs):
        super(DirectoryEntryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'directoryEntryForm'


class OpeningHourForm(forms.ModelForm):
    begins_at = forms.TimeField(
        label="Heure d'ouverture",
        widget=DateTimePicker(options=settings.PICKER_TIME_OPTIONS),
        help_text="Format : HH:MM"
    )

    ends_at = forms.TimeField(
        label="Heure de fermeture",
        widget=DateTimePicker(options=settings.PICKER_TIME_OPTIONS),
        help_text="Format : HH:MM"
    )

    class Meta(object):
        model = OpeningHour
        fields = ['day', 'begins_at', 'ends_at']

    def __init__(self, *args, **kwargs):
        super(OpeningHourForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'openingHourForm'
