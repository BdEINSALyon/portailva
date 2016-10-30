from django.core.exceptions import ValidationError


def validate_passwords(cleaned_data, password_label='password', password_confirm_label='password_confirm'):
    """
    Chek if cleaned_data['password'] == cleaned_data['password_confirm']
    :param cleaned_data:
    :param password_label:
    :param password_confirm_label:
    :return:
    """

    password = cleaned_data.get(password_label)
    password_confirm = cleaned_data.get(password_confirm_label)
    msg = None

    if not password_confirm == password:
        msg = "Les mots de passe sont différents"

        if password_label in cleaned_data:
            del cleaned_data[password_label]

        if password_confirm_label in cleaned_data:
            del cleaned_data[password_confirm_label]

    if msg is not None:
        raise ValidationError(msg)

    return cleaned_data
