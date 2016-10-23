import magic

from crispy_forms.helper import FormHelper
from django import forms

from portailva.association.models import Category, Association
from portailva.file.models import FileVersion


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
        mime = magic.Magic(mime=True)
        if mime.from_file(file.temporary_file_path()) not in [type.mime_type for type in allowed_types]:
            raise forms.ValidationError("Ce type de fichier n'est pas autorisé")

        return file
