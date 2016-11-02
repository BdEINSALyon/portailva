from django.conf import settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, resolve_url
from django.urls import reverse
from django.utils.http import is_safe_url
from django.views.generic import TemplateView, UpdateView

from portailva.member.forms import PasswordUpdateForm, ForgotPasswordForm
from portailva.utils.commons import send_mail
from portailva.utils.mixins import AnonymousRequiredMixin


class LoginView(AnonymousRequiredMixin, TemplateView):
    """Login page for authentication"""
    template_name = 'member/login.html'
    form_class = AuthenticationForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(request)
        return render(request, self.template_name, {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request, data=request.POST)
        redirect_to = request.POST.get('next', request.GET.get('next', ''))

        if form.is_valid():
            auth_login(request, form.get_user())
            return HttpResponseRedirect(self._get_login_redirect_url(request, redirect_to))
        return render(request, self.template_name, {
            'form': form,
            'next': redirect_to,
        })

    def _get_login_redirect_url(self, request, redirect_to):
        # Ensure the user-originating redirection URL is safe.
        if not is_safe_url(url=redirect_to, host=request.get_host()):
            return resolve_url(settings.LOGIN_REDIRECT_URL)
        return redirect_to


class PasswordUpdateView(LoginRequiredMixin, UpdateView):
    """User's settings about his password."""

    form_class = PasswordUpdateForm
    template_name = 'member/password_update.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.user, request.POST)

        if form.is_valid():
            return self.form_valid(form)

        return render(request, self.template_name, {'form': form})

    def form_valid(self, form):
        self.request.user.set_password(form.data.get('password_new'))
        self.request.user.save()
        update_session_auth_hash(self.request, self.request.user)

        send_mail(
            template_html_name='mail/member/reset_password.html',
            template_text_name='mail/member/reset_password.text',
            context={},
            subject="Redéfinition du votre mot de passe",
            to=self.request.user.email
        )

        messages.add_message(self.request, messages.SUCCESS, "Votre mot de passe a été changé avec succès.")

        return redirect(reverse('homepage'))

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=PasswordUpdateForm):
        return form_class(self.get_object())


class ForgotPasswordView(AnonymousRequiredMixin, TemplateView):
    """Allows user to request password change."""
    template_name = 'member/forgot_password.html'
    form_class = ForgotPasswordForm
    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            return self.form_valid(form)
        return render(request, self.template_name, {
            'form': form
        })

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.SUCCESS, "Un courriel contenant de plus amples instructions a été envoyé.")
        return redirect('homepage')
