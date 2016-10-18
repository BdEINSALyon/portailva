from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from .models import File


class FileListView(ListView):
    template_name = 'file/list.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        if not request.user.has_perm('file.can_admin_file'):
            raise PermissionDenied
        return super(FileListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = File.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(FileListView, self).get_context_data(**kwargs)
        return context
