from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import ListView, DeleteView, CreateView

from portailva.file.forms import ResourceFolderForm
from portailva.file.models import ResourceFolder


class ResourceFolderListView(LoginRequiredMixin, ListView):
    model = ResourceFolder

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm('file.manage_resources'):
            raise PermissionDenied
        return super(ResourceFolderListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = ResourceFolder.all_by_tree()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ResourceFolderListView, self).get_context_data(**kwargs)
        return context


class ResourceFolderDeleteView(LoginRequiredMixin, DeleteView):
    model = ResourceFolder

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('file.manage_resources'):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('resource-folder-list')


class ResourceFolderCreateView(LoginRequiredMixin, CreateView):
    http_method_names = ['get', 'post']
    form_class = ResourceFolderForm
    current_folder = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('file.manage_resources'):
            raise PermissionDenied
        return super(ResourceFolderCreateView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.form_class)
        if form.is_valid():
            return self.form_valid(form)
        return render(request, self.template_name, {
            'form': form
        })

    def get_folder(self):
        try:
            folder_pk = int(self.kwargs.get('folder_pk'))
        except (KeyError, ValueError, TypeError):
            return None
        return get_object_or_404(FolderFolder, pk=folder_pk)

    def form_valid(self, form):

        file = ResourceFolder.objects.create(
            name=form.data.get('name'),
            published=True
        )

        # Then file version
        FolderVersion.objects.create(
            version=1,
            data=self.request.FILES['data'],
            file=file,
            user=self.request.user
        )

        return redirect(reverse('resource-folder-list'))
