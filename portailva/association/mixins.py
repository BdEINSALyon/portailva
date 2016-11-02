from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from portailva.association.models import Association


class AssociationMixin(LoginRequiredMixin):
    association = None

    def dispatch(self, request, *args, **kwargs):
        association_pk = int(self.kwargs.get('association_pk', None))
        self.association = get_object_or_404(Association, pk=association_pk)
        if not self.association.can_access(self.request.user):
            raise PermissionDenied

        return super(AssociationMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AssociationMixin, self).get_context_data(**kwargs)
        context['association'] = self.association
        return context
