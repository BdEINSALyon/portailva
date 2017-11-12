import http.client
import time
import urllib.error
import urllib.request

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
        # print('test value', value, flush=True)
        # if value:
        #     req = urllib.request.Request(value)
        #     req.get_method = lambda: 'HEAD'
        #     error_message = ("L'URL saisie ne semble pas pointer vers une image valide. "
        #                      "Assurez-vous que l'URL que vous fournissez ne pointe pas vers une visionneuse "
        #                      "type Google Drive mais bien vers le fichier en lui-même. "
        #                      "Assurez-vous également que l'accès à l'image ne requière pas "
        #                      "d'authentification (mode \"public\" sur PortailVA).")
        #     print('req url', req.full_url, flush=True)
        #     print('req method', req.get_method(), flush=True)
        #     try:
        #         print('before urlopen', flush=True)
        #         res = urllib.request.urlopen(req)  # type: http.client.HTTPResponse
        #         print('after urlopen', flush=True)
        #     except urllib.error.HTTPError as err:
        #         raise ValidationError(error_message)
        #     else:
        #         print('status_code', res.getcode(), flush=True)
        #         print('headers', res.getheaders(), flush=True)
        #         if 'image' not in res.getheader('Content-Type'):
        #             raise ValidationError(error_message)
        return value
