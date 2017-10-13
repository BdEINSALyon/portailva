import re

import requests
from django.core.exceptions import ValidationError


def validate_image_url(url):
    if not url:
        return url

    res = requests.get(url)
    if 'image' not in res.headers.get('Content-Type'):
        raise ValidationError("L'URL saisie ne semble pas pointer vers une image valide. "
                              "Assurez-vous que l'URL que vous fournissez ne pointe pas vers une visionneuse "
                              "type Google Drive mais bien vers le fichier en lui-même. "
                              "Assurez-vous également que l'accès à l'image ne requière pas "
                              "d'authentification (mode \"public\" sur PortailVA).")
