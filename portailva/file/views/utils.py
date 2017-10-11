from django.urls import reverse
from django.views import View

from portailva.file.models import ResourceFolder, ResourceFile


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
            return self._get_folder().resources.all().order_by('name')
        else:
            return ResourceFile.objects.filter(folder=None)

    def _get_folders(self):
        """
        List folders contained into the current directory.
        If the current directory is None, it list folders on root directory.
        A folder on root directory is a file without any parent.
        """
        if self.kwargs['folder_pk'] is not None:
            return self._get_folder().children.all().order_by('name')
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
