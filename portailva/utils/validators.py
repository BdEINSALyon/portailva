import re

import requests
from django.core.exceptions import ValidationError


def validate_image_url(url):
    res = requests.head(url, allow_redirects=True)
    if 'image' not in res.headers.get('Content-Type'):
        raise ValidationError("L'URL saisie ne semble pas pointer vers une image valide. "
                              "Assurez-vous que l'URL que vous fournissez ne pointe pas vers une visionneuse "
                              "type Google Drive mais bien vers le fichier en lui-même. "
                              "Assurez-vous également que l'accès à l'image ne requière pas "
                              "d'authentification (mode \"public\" sur PortailVA).")


def validate_iban(iban):
    fr_iban_re = re.compile(r'^FR[0-9A-Z]{25}$')
    if not fr_iban_re.match(iban):
        raise ValidationError("L'IBAN saisi n'est pas valide. "
                                    "Il doit commencer par FR et ne contenir que "
                                    "des lettres majuscules ou des chiffres (pas d'espace, de tirets, ...). "
                                    "27 caractères au total.")

    verif_iban = list(iban[4:] + iban[:4])
    verif_iban_num = ''
    for c in verif_iban:
        if 'A' <= c <= 'Z':
            c = str(ord(c) - ord('A') + 10)
        verif_iban_num += c
    verif_iban_num = int(verif_iban_num)

    if verif_iban_num % 97 != 1:
        raise ValidationError("L'IBAN saisi a la bonne forme mais n'est pas valide.")
