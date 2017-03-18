from bootstrap3_datetime.widgets import DateTimePicker
from crispy_forms.helper import FormHelper
from django import forms
from django.conf import settings

from .models import Category, Association, Mandate, People


class AssociationForm(forms.ModelForm):
    class Meta:
        fields = ['category', 'name', 'acronym', 'description', 'active_members_number']
        model = Association

    def __init__(self, *args, **kwargs):
        super(AssociationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'associationForm'


class AssociationAdminForm(AssociationForm):
    is_active = forms.BooleanField(
        label="Association active ?",
        required=False,
        initial=True
    )


class MandateForm(forms.Form):
    begins_at = forms.DateField(
        label="Début de mandat",
        widget=DateTimePicker(options=settings.PICKER_DATE_OPTIONS),
        help_text="Format : JJ/MM/AAAA"
    )

    ends_at = forms.DateField(
        label="Fin de mandat",
        widget=DateTimePicker(options=settings.PICKER_DATE_OPTIONS),
        help_text="Format : JJ/MM/AAAA"
    )

    def __init__(self, *args, **kwargs):
        self.association = kwargs.pop('association', None)
        super(MandateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'mandateForm'

    def clean(self):
        super(MandateForm, self).clean()
        begins_at = self.cleaned_data['begins_at']
        ends_at = self.cleaned_data['ends_at']

        # We ensure begins_at is strictly before ends_at
        if begins_at >= ends_at:
            raise forms.ValidationError("La date de fin ne peut ni être égale ni être antérieure à la date de début.")

        # We ensure there is no other mandate during the same time as defined by the user
        association_mandates = Mandate.objects.all().filter(association_id=self.association.id)
        for mandate in association_mandates:
            if begins_at <= mandate.begins_at < ends_at or begins_at < mandate.ends_at <= ends_at:
                raise forms.ValidationError("La période définie pour ce mandat empiète sur la période d'un autre "
                                            "mandat.")


class PeopleForm(forms.ModelForm):
    class Meta(object):
        model = People
        fields = ['first_name', 'last_name', 'email', 'phone', 'role']

    def __init__(self, *args, **kwargs):
        super(PeopleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'peopleForm'
