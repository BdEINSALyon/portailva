from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic import UpdateView

from portailva.association.forms import AssociationUpdateForm
from portailva.association.models import Association


class AssociationDetailView(DetailView):
    model = Association
    template_name = 'association/detail.html'
    object = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.can_access(request.user):
            raise PermissionDenied
        return super(AssociationDetailView, self).get(request, *args, **kwargs)


class AssociationUpdateView(UpdateView):
    template_name = 'association/update.html'
    form_class = AssociationUpdateForm
    model = Association
    object = None

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.can_access(request.user):
            raise PermissionDenied
        return super(AssociationUpdateView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.create_form(self.form_class, **{
            'name': self.object.name,
            'category': self.object.category,
            'acronym': self.object.acronym,
            'description': self.object.description
        })

        return render(request, self.template_name, {'association': self.object, 'form': form})

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.form_class)
        if form.is_valid():
            return self.form_valid(form)
        return render(request, self.template_name, {'association': self.object, 'form': form})

    def create_form(self, form_class, **kwargs):
        return form_class(initial=kwargs)

    def get_form(self, form_class=None):
        return form_class(self.request.POST)

    def form_valid(self, form):
        self.object.name = form.data.get('name')
        self.object.type = form.data.get('category')
        self.object.acronym = form.data.get('acronym')
        self.object.description = form.data.get('description')

        self.object.save()

        return redirect(reverse('association-detail', kwargs={'pk': self.object.id}))