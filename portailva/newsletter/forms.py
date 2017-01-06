from bootstrap3_datetime.widgets import DateTimePicker
from crispy_forms.helper import FormHelper
from django import forms
from django.conf import settings
from django.utils.datetime_safe import datetime

from .models import Article


class ArticleForm(forms.ModelForm):

    class Meta(object):
        model = Article
        fields = ('title', 'content',)

    def __init__(self, *args, **kwargs):
        self.association = kwargs.pop('association', None)
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'articleForm'

    def save(self, commit=True):
        self.instance.association_id = self.association.id
        return super(ArticleForm, self).save(commit)
