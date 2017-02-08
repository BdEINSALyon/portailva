from bootstrap3_datetime.widgets import DateTimePicker
from crispy_forms.helper import FormHelper
from django import forms
from django.conf import settings
from django.utils.datetime_safe import datetime

from .models import Article, Newsletter


class ArticleForm(forms.ModelForm):

    class Meta(object):
        model = Article
        fields = ('title', 'featured_image', 'short_content', 'content',)

    short_content = forms.CharField(widget=forms.Textarea, label="Brève de l'article",
                                    help_text="Ce texte est affiché dans la newsletter VA. Il est limité à 255 "
                                              "caractères. Les retours à la ligne sont tolérés.")

    def __init__(self, *args, **kwargs):
        self.association = kwargs.pop('association', None)
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'articleForm'

    def save(self, commit=True):
        self.instance.association_id = self.association.id
        return super(ArticleForm, self).save(commit)


class NewsletterForm(forms.ModelForm):

    class Meta(object):
        model = Newsletter
        fields = ('title', 'sent', 'articles', 'events')

    def __init__(self, *args, **kwargs):
        super(NewsletterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'newsletterForm'

