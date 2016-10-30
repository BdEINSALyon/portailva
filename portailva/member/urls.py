from django.conf.urls import url
from django.contrib.auth import views as auth_views

from portailva.member.views import PasswordUpdateView

urlpatterns = [
    url(r'^login/$', auth_views.login, name='member-login'),
    url(r'^logout/$', auth_views.logout, name='member-logout'),

    url(r'^change-password/$', PasswordUpdateView.as_view(), name='member-change-password')
]
