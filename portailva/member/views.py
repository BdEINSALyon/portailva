from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import UpdateView

from portailva.member.forms import PasswordUpdateForm


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
        return redirect(reverse('homepage'))

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=PasswordUpdateForm):
        return form_class(self.get_object())
