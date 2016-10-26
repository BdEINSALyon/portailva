import magic

from crispy_forms.helper import FormHelper
from django import forms

from portailva.association.models import Category, Association, Mandate
from portailva.settings import MAGIC_BIN


class AssociationForm(forms.Form):
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


class AssociationFileUploadForm(forms.Form):
    name = forms.CharField(
        label="Nom",
        max_length=255
    )

    data = forms.FileField(
        label="Fichier"
    )

    def __init__(self, *args, **kwargs):
        self.folder = kwargs.pop('folder', None)
        super(AssociationFileUploadForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'associationForm'

    def clean_data(self):
        file = self.cleaned_data['data']

        # We ensure file have correct mime type
        allowed_types = self.folder.allowed_types.all()
        mime = magic.Magic(mime=True, magic_file=MAGIC_BIN)
        if mime.from_file(file.temporary_file_path()) not in [type.mime_type for type in allowed_types]:
            raise forms.ValidationError("Ce type de fichier n'est pas autorisé")

        return file


class MandateForm(forms.Form):
    begins_at = forms.DateField(
        label="Début de mandat",
        input_formats=[
            '%Y-%m-%d',
            '%d/%m/%Y',
            '%d/%m/%y'
        ],
        widget=forms.TextInput(
            attrs={'type': 'date'}
        ),
        help_text="Format : JJ/MM/AAAA"
    )

    ends_at = forms.DateField(
        label="Fin de mandat",
        input_formats=[
            '%Y-%m-%d',
            '%d/%m/%Y',
            '%d/%m/%y'
        ],
        widget=forms.TextInput(
            attrs={'type': 'date'}
        ),
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
