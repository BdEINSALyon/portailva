import requests
import time
from crispy_forms.helper import FormHelper
from django import forms
from django.core.exceptions import ValidationError

from portailva.utils.models import Place


class PlaceForm(forms.ModelForm):
    class Meta(object):
        model = Place
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PlaceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'placeForm'


class ImageURLField(forms.URLField):
    def clean(self, value):
        value = super().clean(value)
        print('test value', value)
        print('sleeping 2 sec')
        time.sleep(2)
        print('slept')
        if value:
            res = requests.get(value)
            print('status_code', res.status_code)
            print('headers', res.headers)
            if 'image' not in res.headers.get('Content-Type'):
                raise ValidationError("L'URL saisie ne semble pas pointer vers une image valide. "
                                      "Assurez-vous que l'URL que vous fournissez ne pointe pas vers une visionneuse "
                                      "type Google Drive mais bien vers le fichier en lui-même. "
                                      "Assurez-vous également que l'accès à l'image ne requière pas "
                                      "d'authentification (mode \"public\" sur PortailVA).")
        return value
