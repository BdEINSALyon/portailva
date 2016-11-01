from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from django.views.generic.edit import CreateView, FormMixin, ProcessFormView

from portailva.member.forms import PasswordUpdateForm, ForgotPasswordForm
from portailva.utils.commons import send_mail


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


class ForgotPasswordView(TemplateView):
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
