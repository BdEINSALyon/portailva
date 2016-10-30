from crispy_forms.helper import FormHelper
from django import forms


# Max password length for the user.
from django.contrib.auth import authenticate

from portailva.member.validators import validate_passwords

MAX_PASSWORD_LENGTH = 76
# Min password length for the user.
MIN_PASSWORD_LENGTH = 6


class PasswordUpdateForm(forms.Form):

    password_old = forms.CharField(
        label="Mot de passe actuel",
        widget=forms.PasswordInput,
    )

    password_new = forms.CharField(
        label="Nouveau mot de passe",
        max_length=MAX_PASSWORD_LENGTH,
        min_length=MIN_PASSWORD_LENGTH,
        widget=forms.PasswordInput
    )

    password_confirm = forms.CharField(
        label="Confirmer le nouveau mot de passe",
        max_length=MAX_PASSWORD_LENGTH,
        min_length=MIN_PASSWORD_LENGTH,
        widget=forms.PasswordInput
    )

    def __init__(self, user, *args, **kwargs):
        super(PasswordUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'passwordForm'

        self.user = user

    def clean(self):
        cleaned_data = super(PasswordUpdateForm, self).clean()

        password_old = cleaned_data.get('password_old')

        # Check if the current password is not empty
        if password_old:
            user_exist = authenticate(username=self.user.email, password=password_old)
            # Check if the user exist with old information.
            if not user_exist and password_old != '':
                self._errors['password_old'] = self.error_class(["Mot de passe incorrect."])
                if 'password_old' in cleaned_data:
                    del cleaned_data['password_old']

        return validate_passwords(cleaned_data, password_label='password_new')

