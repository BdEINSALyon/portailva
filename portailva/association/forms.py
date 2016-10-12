from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from portailva.association.models import Category, Association


class AssociationUpdateForm(forms.Form):
    category = forms.ModelChoiceField(
        label="Catégorie",
        queryset=Category.objects.all()
    )

    name = forms.CharField(
        label="Nom",
        max_length=Association._meta.get_field('name').max_length,
    )

    acronym = forms.CharField(
        label="Acronyme",
        max_length=Association._meta.get_field('acronym').max_length,
        required=False
    )

    description = forms.CharField(
        label="Description courte",
        help_text="Cette description n'est pas visible dans le Bot'INSA",
        widget=forms.Textarea()
    )

    def __init__(self, *args, **kwargs):
        super(AssociationUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'updateForm'

        self.helper.add_input(Submit('submit', 'Envoyer'))