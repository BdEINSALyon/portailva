import magic

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView

from portailva.association.mixins import AssociationMixin
from .forms import AssociationFileUploadForm
from .models import File, FileVersion, FileFolder, AssociationFile


class FileListView(LoginRequiredMixin, ListView):
    template_name = 'file/list.html'

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

            mime = magic.Magic(mime=True, magic_file=settings.MAGIC_BIN)
            mime_type = mime.from_file(version.data.url)

            response = HttpResponse(version.data.read(), content_type=mime_type)
            return response
        except FileVersion.DoesNotExist:
            raise Http404


# Association files
class AssociationFileTreeView(AssociationMixin, DetailView):
    template_name = 'association/files.html'

    def get(self, request, *args, **kwargs):
        try:
            folder_pk = int(self.kwargs.get('folder_pk'))
            current_folder = FileFolder.objects.get(pk=folder_pk)
            folders = FileFolder.objects.all().filter(parent_id=current_folder.id).order_by('name')
            files = AssociationFile.objects.all()\
                .filter(association_id=self.association.id)\
                .filter(folder_id=folder_pk)\
                .order_by('name')
        except (KeyError, ValueError, TypeError):
            # User wants to list folders on root folder
            folders = FileFolder.objects.all().filter(parent=None).order_by('name')
            files = list()
            current_folder = None
        except:
            raise Http404

        return render(request, self.template_name, {
            'association': self.association,
            'folders': folders,
            'files': files,
            'current_folder': current_folder
        })

    def get_folder(self):
        try:
            folder_pk = int(self.kwargs.get('folder_pk'))
        except (KeyError, ValueError, TypeError):
            return None
        return get_object_or_404(FileFolder, pk=folder_pk)


class AssociationFileUploadView(AssociationMixin, CreateView):
    template_name = 'association/file_upload.html'
    http_method_names = ['get', 'post']
    form_class = AssociationFileUploadForm
    current_folder = None

    def dispatch(self, request, *args, **kwargs):
        try:
            folder_pk = int(self.kwargs.get('folder_pk'))
            self.current_folder = FileFolder.objects.get(pk=folder_pk)
            if not self.current_folder.is_writable:
                # User can't upload file here
                raise Http404
        except:
            # Folder id not provided or folder does not exist
            raise Http404

        return super(AssociationFileUploadView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'form': self.form_class(),
            'association': self.association,
            'current_folder': self.current_folder
        })

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.form_class)
        if form.is_valid():
            return self.form_valid(form)
        return render(request, self.template_name, {
            'association': self.association,
            'form': form,
            'current_folder': self.current_folder
        })

    def get_form(self, form_class=AssociationFileUploadForm):
        return form_class(data=self.request.POST, files=self.request.FILES, folder=self.current_folder)

    def get_folder(self):
        try:
            folder_pk = int(self.kwargs.get('folder_pk'))
        except (KeyError, ValueError, TypeError):
            return None
        return get_object_or_404(FileFolder, pk=folder_pk)

    def form_valid(self, form):
        # We first create file
        file = AssociationFile.objects.create(
            name=form.data.get('name'),
            association=self.association,
            folder=self.current_folder
        )

        # Then file version
        FileVersion.objects.create(
            version=1,
            data=self.request.FILES['data'],
            file=file,
            user=self.request.user
        )

        return redirect(reverse('association-file-tree', kwargs={
            'association_pk': self.association.id,
            'folder_pk': self.current_folder.id
        }))


class AssociationFileDeleteView(AssociationMixin, DeleteView):
    model = AssociationFile
    template_name = 'association/file_delete.html'
    success_url = None

    def post(self, request, *args, **kwargs):
        self.success_url = reverse('association-file-tree', kwargs={
            'association_pk': self.association.id,
            'folder_pk': self.get_object().folder_id
        })

        messages.add_message(self.request, messages.SUCCESS, "Le fichier a correctement été supprimé.")

        return super(AssociationFileDeleteView, self).post(request, *args, **kwargs)
