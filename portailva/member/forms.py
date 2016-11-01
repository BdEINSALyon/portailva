from crispy_forms.bootstrap import StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML, ButtonHolder
from django import forms


# Max password length for the user.
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from portailva.member.validators import validate_passwords
from portailva.utils.commons import send_mail

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


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label="Adresse email"
    )

    def __init__(self, *args, **kwargs):
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'forgotForm'

    def get_users(self, email):
        active_users = get_user_model()._default_manager.filter(
            email__iexact=email, is_active=True)
        return (u for u in active_users if u.has_usable_password())

    def save(self):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        email = self.cleaned_data["email"]
        for user in self.get_users(email):

            # For each user, we generate a token
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)

            # We make the reset URL to be sent by mail
            reset_url = settings.PORTAILVA_APP['site']['url'] + reverse('member-reset-password-confirm', kwargs={
                'uidb64': uid,
                'token': token
            })

            # Then we send the mail
            context = {
                'reset_url': reset_url
            }

            send_mail(
                template_html_name='mail/member/reset_password.html',
                template_text_name='mail/member/reset_password.text',
                context=context,
                subject="Réinitialisation du mot de passe",
                to=user.email
            )


class ResetPasswordForm(SetPasswordForm):
    def __init__(self, user, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(user, *args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Field('new_password1'),
            Field('new_password2'),
            HTML('{% csrf_token %}'),
            ButtonHolder(
                StrictButton("Enregistrer", type='submit'),
            )
        )
