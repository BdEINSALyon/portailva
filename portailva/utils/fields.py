from django.db.models import URLField
from . import forms

from portailva.utils.validators import validate_image_url


class ImageURLField(URLField):
    def __init__(self, *args, **kwargs):
        kwargs['validators'] = [validate_image_url]
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.ImageURLField,
        }
        defaults.update(kwargs)
        return super(URLField, self).formfield(**defaults)


class LogoURLField(ImageURLField):
    def __init__(self, *args, **kwargs):
        kwargs['help_text'] = ("Privilégiez les liens en HTTPS. "
                               "Assurez-vous que le lien que vous fournissez "
                               "pointe directement sur l'image (pas de page "
                               "d'affichage comme Google Drive ou autres) et que "
                               "l'image soit accessible.")
        super().__init__(*args, **kwargs)
