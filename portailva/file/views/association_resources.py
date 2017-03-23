from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView

from portailva.association.mixins import AssociationMixin
from portailva.file.views.utils import FolderScoped


class AssocitationResourceView(AssociationMixin, FolderScoped, TemplateView):
    template_name = 'file/resources/folders/list_associations.html'

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm('file.manage_resources'):
            raise PermissionDenied
        return super(AssocitationResourceView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AssocitationResourceView, self).get_context_data(**kwargs)
        context['current_folder'] = self._get_folder()
        context['files'] = self._get_files()
        context['folders'] = self._get_folders()
        return context
