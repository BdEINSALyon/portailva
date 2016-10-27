from crispy_forms.helper import FormHelper
from django import forms

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
