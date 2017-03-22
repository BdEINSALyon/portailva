from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView

from portailva.file.models import File


class FileListView(LoginRequiredMixin, ListView):
    template_name = 'file/files/list.html'

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm('file.admin_file'):
            raise PermissionDenied
        return super(FileListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = File.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(FileListView, self).get_context_data(**kwargs)
        return context
