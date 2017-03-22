from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import DeleteView, CreateView, TemplateView

from portailva.file.forms import ResourceFolderForm, ResourceFileForm
from portailva.file.models import ResourceFolder, ResourceFile, FileVersion


class FolderScoped(View):
    """
    Define a view where the path argument may contains a folder.
    The path argument "folder_pk" is used as the id of current folder.
    The class contains useful functions to retrieve current folder, files and sub-folders.
    """
    def _get_folder(self):
        """Get current folder or None if there is not"""
        if self.kwargs['folder_pk'] is not None:
            return ResourceFolder.objects.get(pk=self.kwargs['folder_pk'])
        else:
            return None

    def _get_files(self):
        """
        List files contained into the current directory.
        If the current directory is None, it list files on root directory.
        A file on root directory is a file without folder.
        """
        if self.kwargs['folder_pk'] is not None:
            return self._get_folder().resources.all()
        else:
            return ResourceFile.objects.filter(folder=None)

    def _get_folders(self):
        """
        List folders contained into the current directory.
        If the current directory is None, it list folders on root directory.
        A folder on root directory is a file without any parent.
        """
        if self.kwargs['folder_pk'] is not None:
            return self._get_folder().children.all()
        else:
            return ResourceFolder.objects.filter(parent=None)

    def url(self):
        """
        Generate URL to the current folder.
        It can be used to redirect the user to the current folder after a form or deletion.
        :return: the string path computed by reverse django method
        """
        folder = self._get_folder()
        if folder is None:
            return reverse('resource-folder-list')
        else:
            return reverse('resource-folder-list', kwargs={'folder_pk': folder.id})


class ResourceFolderListView(LoginRequiredMixin, TemplateView, FolderScoped):
    model = ResourceFolder
    template_name = 'file/resources/folders/list.html'

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm('file.manage_resources'):
            raise PermissionDenied
        return super(ResourceFolderListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ResourceFolderListView, self).get_context_data(**kwargs)
        context['folder'] = self._get_folder()
        context['files'] = self._get_files()
        context['folders'] = self._get_folders()
        context['new_file'] = ResourceFileForm(folder=context['folder'])
        context['new_folder'] = ResourceFolderForm(folder=context['folder'])
        return context


class UploadResourceView(LoginRequiredMixin, FolderScoped, View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        if not request.user.has_perm('file.manage_resources'):
            raise PermissionDenied

        folder = self._get_folder()
        form = ResourceFileForm(folder=folder, data=self.request.POST, files=self.request.FILES)
        file_name = request.FILES['data'].name
        files = ResourceFile.objects.filter(folder=folder, name=file_name).first()
        if files is not None:
            messages.add_message(request, messages.ERROR, 'Un fichier existe déjà avec ce nom')
        elif form.is_valid():
            file = ResourceFile.objects.create(
                name=file_name,
                published=True,
                folder=folder
            )
            # Then file version
            FileVersion.objects.create(
                version=1,
                data=self.request.FILES['data'],
                file=file,
                user=self.request.user
            )
            messages.add_message(request, messages.SUCCESS, 'Fichier enregistré')
        else:
            messages.add_message(request, messages.ERROR, 'Ce fichier ne peut pas être sauvegardé')
        return redirect(self.url())


class CreateResourceFolderView(LoginRequiredMixin, FolderScoped, View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        if not request.user.has_perm('file.manage_resources'):
            raise PermissionDenied

        parent = self._get_folder()
        form = ResourceFolderForm(folder=parent, data=self.request.POST)

        folder = ResourceFolder.objects.filter(parent=parent, name=form.data['name']).first()
        if folder is not None:
            messages.add_message(request, messages.ERROR, 'Un dossier existe déjà avec ce nom')
        else:
            folder = ResourceFolder.objects.create(
                name=form.data['name'],
                parent=parent
            )
            messages.add_message(request, messages.SUCCESS, 'Dossier créé')
        return redirect(reverse('resource-folder-list', kwargs={'folder_pk': folder.id}))


class ResourceFolderDeleteView(LoginRequiredMixin, FolderScoped, DeleteView):
    http_method_names = ['get', 'post']
    model = ResourceFolder
    template_name = "file/resources/folders/delete.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('file.manage_resources'):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.url()


class ResourceFileDeleteView(LoginRequiredMixin, FolderScoped, DeleteView):
    http_method_names = ['get', 'post']
    model = ResourceFile
    template_name = "file/resources/files/delete.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('file.manage_resources'):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.url()
