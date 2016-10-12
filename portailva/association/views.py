from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView

from portailva.association.models import Association


class AssociationDetailView(DetailView):
    model = Association
    template_name = 'association/detail.html'
    object = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(AssociationDetailView, self).get(request, *args, **kwargs)