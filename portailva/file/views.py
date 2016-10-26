import magic
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic import ListView

from portailva.settings import MAGIC_BIN
from .models import File, FileVersion


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


class FileView(DetailView):
    template_name = None
    model = File
    object = None

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.can_access(request.user):
            raise PermissionDenied
        return super(FileView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # We get file last version
        try:
            version = FileVersion.objects\
                .filter(file_id=self.object.id)\
                .latest('created_at')

            mime = magic.Magic(mime=True, magic_file=MAGIC_BIN)
            mime_type = mime.from_file(version.data.url)

            response = HttpResponse(version.data.read(), content_type=mime_type)
            return response
        except FileVersion.DoesNotExist:
            raise Http404
