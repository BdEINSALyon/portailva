from django.conf.urls import url
from django.contrib.auth import views as auth_views

from portailva.member.forms import ResetPasswordForm
from portailva.member.views import PasswordUpdateView, ForgotPasswordView, LoginView

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='member-login'),
    url(r'^logout/$', auth_views.logout, name='member-logout'),

    url(r'^forgot-password/$', ForgotPasswordView.as_view(), name='member-forgot-password'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, {
            'template_name': 'member/password_reset.html',
            'post_reset_redirect': 'homepage',
            'set_password_form': ResetPasswordForm
         }, name='member-reset-password-confirm'),
    url(r'^change-password/$', PasswordUpdateView.as_view(), name='member-change-password')

]
