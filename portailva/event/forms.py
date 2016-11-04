from bootstrap3_datetime.widgets import DateTimePicker
from crispy_forms.helper import FormHelper
from django import forms
from django.conf import settings
from django.utils.datetime_safe import datetime

from .models import Event, EventPrice


class EventForm(forms.ModelForm):
    short_description = forms.CharField(
        label="Description courte",
        help_text=str(Event._meta.get_field('short_description').max_length) + " caractères max.",
        widget=forms.Textarea()
    )

    begins_at = forms.DateTimeField(
        label="Date et heure de début",
        help_text="Format : " + settings.PICKER_DATETIME_OPTIONS['format'],
        widget=DateTimePicker(options=settings.PICKER_DATETIME_OPTIONS)

    )

    ends_at = forms.DateTimeField(
        label="Date et heure de fin",
        help_text="Format : " + settings.PICKER_DATETIME_OPTIONS['format'],
        widget=DateTimePicker(options=settings.PICKER_DATETIME_OPTIONS)
    )

    class Meta(object):
        model = Event
        fields = ('type', 'name', 'short_description', 'description', 'place', 'begins_at', 'ends_at',)

    def __init__(self, *args, **kwargs):
        self.association = kwargs.pop('association', None)
        super(EventForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'eventForm'

    def clean_ends_at(self):
        ends_at = self.cleaned_data['ends_at']
        begins_at = self.cleaned_data['begins_at']

        if ends_at.replace(tzinfo=None) <= datetime.now().replace(tzinfo=None):
            raise forms.ValidationError("Vous ne pouvez pas créer d'événement dans le passé.")

        if begins_at >= ends_at:
            raise forms.ValidationError("La date de fin doit être ultérieure à la date de début.")

        return self.cleaned_data['ends_at']

    def save(self, commit=True):
        self.instance.association_id = self.association.id
        return super(EventForm, self).save(commit)


class EventPriceForm(forms.ModelForm):
    name = forms.CharField(
        label="Nom du tarif",
        max_length=EventPrice._meta.get_field('name').max_length,
        widget=forms.TextInput(attrs={'placeholder': "Ex : plein tarif, Tarif VA, etc."})
    )
    price = forms.DecimalField(
        label="Tarif",
        initial=0.0,
        help_text="Valeur en €. Mettre 0 pour gratuit."
    )

    class Meta(object):
        model = EventPrice
        fields = ('name', 'price', 'is_va', 'is_variable',)

    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop('event', None)
        super(EventPriceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'eventPriceForm'

    def save(self, commit=True):
        self.instance.event_id = self.event.id
        return super(EventPriceForm, self).save(commit)
