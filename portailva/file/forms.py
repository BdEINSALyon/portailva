import magic

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django import forms
from django.conf import settings
from django.urls import reverse

from portailva.file.models import ResourceFolder, ResourceFile


class AssociationFileUploadForm(forms.Form):
    name = forms.CharField(
        label="Nom",
        max_length=255
    )

    data = forms.FileField(
        label="Fichier",
        help_text="Taille maximum : " + str(settings.PORTAILVA_APP['file']['file_max_size'] // (1024 * 1024)) + "Mo"
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
        mime = magic.Magic(mime=True, magic_file=settings.MAGIC_BIN)
        if mime.from_file(file.temporary_file_path()) not in [type.mime_type for type in allowed_types]:
            raise forms.ValidationError("Ce type de fichier n'est pas autorisé")

        if file is not None and file.size > settings.PORTAILVA_APP['file']['file_max_size']:
            raise forms.ValidationError("Votre fichier est trop lourd, la limite autorisée est de " +
                                        str(settings.PORTAILVA_APP['file']['file_max_size'] // (1024 * 1024)) + "Mo")

        return file


class ResourceFileUploadForm(forms.Form):
    name = forms.CharField(
        label="Nom",
        max_length=255
    )

    data = forms.FileField(
        label="Fichier",
        help_text="Taille maximum : " + str(settings.PORTAILVA_APP['file']['file_max_size'] // (1024 * 1024)) + "Mo"
    )

    def __init__(self, *args, **kwargs):
        super(ResourceFileUploadForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'associationForm'

    def clean_data(self):
        file = self.cleaned_data['data']

        if file is not None and file.size > settings.PORTAILVA_APP['file']['file_max_size']:
            raise forms.ValidationError("Votre fichier est trop lourd, la limite autorisée est de " +
                                        str(settings.PORTAILVA_APP['file']['file_max_size'] // (1024 * 1024)) + "Mo")

        return file


class ResourceFolderForm(forms.ModelForm):
    class Meta:
        model = ResourceFolder
        fields = ('name', 'parent')
        widgets = {'parent': forms.HiddenInput()}

    def __init__(self, folder, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'resource-folder-form'
        if folder is None:
            self.helper.form_action = reverse('resource-folder-create')
        else:
            self.helper.form_action = reverse('resource-folder-create', kwargs={'folder_pk': folder.id})
        super(ResourceFolderForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Créer le dossier'))


class ResourceFileForm(forms.Form):

    data = forms.FileField(
        label="Fichier",
        help_text="Taille maximum : " + str(settings.PORTAILVA_APP['file']['file_max_size'] // (1024 * 1024)) + "Mo"
    )

    def __init__(self, folder, *args, **kwargs):
        super(ResourceFileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        if folder is None:
            self.helper.form_action = reverse('resource-upload')
        else:
            self.helper.form_action = reverse('resource-upload', kwargs={'folder_pk': folder.id})
        self.helper.add_input(Submit('submit', 'Envoyer le fichier'))

    def clean_data(self):
        file = self.cleaned_data['data']

        if file is not None and file.size > settings.PORTAILVA_APP['file']['file_max_size']:
            raise forms.ValidationError("Votre fichier est trop lourd, la limite autorisée est de " +
                                        str(settings.PORTAILVA_APP['file']['file_max_size'] // (1024 * 1024)) + "Mo")

        return file
