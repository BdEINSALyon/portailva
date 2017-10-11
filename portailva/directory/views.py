from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, TemplateView, UpdateView, ListView

from portailva.association.mixins import AssociationMixin
from portailva.association.models import Association
from .forms import DirectoryEntryForm, OpeningHourForm
from .models import DirectoryEntry, OpeningHour
from .mixins import AssociationDirectoryEntryMixin, OpeningHourMixin


class AssociationDirectoryEntryDetailView(AssociationDirectoryEntryMixin, DetailView):
    model = DirectoryEntry
    template_name = 'directory/detail.html'


class AssociationDirectoryEntryUpdateView(AssociationDirectoryEntryMixin, UpdateView):
    model = DirectoryEntry
    form_class = DirectoryEntryForm
    template_name = 'directory/update.html'

    def form_valid(self, form):
        if self.object is not None and not self.object.is_online:
            # This version is not yet online, so we can update it.
            directory_entry = form.save(commit=False)
            directory_entry.association = self.association
            directory_entry.save()
        else:
            # Version is already online or doesn't exist, we create a new one
            directory_entry = DirectoryEntry.objects.create(
                description=form.data.get('description'),
                contact_address=form.data.get('contact_address'),
                phone=form.data.get('phone'),
                website_url=form.data.get('website_url'),
                facebook_url=form.data.get('facebook_url'),
                twitter_url=form.data.get('twitter_url'),
                association_id=self.association.id,
                place_id=form.data.get('place')
            )

            if self.object is not None:
                # We copy opening hours
                for opening_hour in self.object.opening_hours.all():
                    opening_hour.pk = None
                    opening_hour.directory_entry_id = directory_entry.id
                    opening_hour.save()

        return redirect(reverse('association-directory-detail', kwargs={
            'association_pk': self.association.id
        }))


class AssociationDirectoryEntryOpeningHourCreateView(AssociationDirectoryEntryMixin, CreateView):
    form_class = OpeningHourForm
    template_name = 'directory/opening_hour/new.html'

    def form_valid(self, form):
        directory_entry = self.get_object()
        if directory_entry.is_online:
            # Version is already online, we create a new one before adding opening hour
            opening_hours = directory_entry.opening_hours.all()
            directory_entry.pk = None
            directory_entry.is_online = False
            directory_entry.save()

            # We copy existing opening hours
            for opening_hour in opening_hours:
                opening_hour.pk = None
                opening_hour.directory_entry_id = directory_entry.id
                opening_hour.save()

        # We create opening hour
        OpeningHour.objects.create(
            day=form.cleaned_data.get('day'),
            begins_at=form.cleaned_data.get('begins_at'),
            ends_at=form.cleaned_data.get('ends_at'),
            directory_entry_id=directory_entry.id
        )

        return redirect(reverse('association-directory-detail', kwargs={
            'association_pk': self.association.id
        }))


class AssociationDirectoryEntryOpeningHourUpdateView(OpeningHourMixin, UpdateView):
    form_class = OpeningHourForm
    template_name = 'directory/opening_hour/update.html'
    directory_entry = None

    def form_valid(self, form):
        directory_entry = self.object.directory_entry
        opening_hour = form.save(commit=False)

        if directory_entry.is_online:
            # We have to create a new directory entry
            opening_hours = directory_entry.opening_hours.all()
            directory_entry.pk = None
            directory_entry.is_online = False
            directory_entry.save()

            # We duplicate each opening hour, except which one we want to update
            for row in opening_hours:
                if row.id != opening_hour.id:
                    row.pk = None
                    row.directory_entry_id = directory_entry.id
                    row.save()

            # Then we process opening hour we want to update
            opening_hour.pk = None
            opening_hour.directory_entry_id = directory_entry.id

        opening_hour.day = form.cleaned_data.get('day')
        opening_hour.begins_at = form.cleaned_data.get('begins_at')
        opening_hour.ends_at = form.cleaned_data.get('ends_at')
        opening_hour.save()

        return redirect(reverse('association-directory-detail', kwargs={
            'association_pk': self.association.id
        }))


class AssociationDirectoryEntryOpeningHourDeleteView(OpeningHourMixin, DeleteView):
    form_class = OpeningHourForm
    template_name = 'directory/opening_hour/delete.html'
    directory_entry = None

    def post(self, request, *args, **kwargs):
        opening_hour = self.get_object()
        directory_entry = opening_hour.directory_entry

        if directory_entry.is_online:
            # We have to create a new directory entry
            opening_hours = directory_entry.opening_hours.all()
            directory_entry.pk = None
            directory_entry.is_online = False
            directory_entry.save()

            # We duplicate each opening hour, except which one we want to delete
            for row in opening_hours:
                if row.id != opening_hour.id:
                    row.pk = None
                    row.directory_entry_id = directory_entry.id
                    row.save()
        else:
            opening_hour.delete()

        return redirect(reverse('association-directory-detail', kwargs={
            'association_pk': self.association.id
        }))


class AssociationDirectoryEntryPublishView(AssociationMixin, TemplateView):
    template_name = 'directory/publish.html'
    http_method_names = ['get', 'post']

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('directory.admin_directoryentry'):
            raise PermissionDenied
        self.object = DirectoryEntry.objects.get_last_for_association_id(kwargs.get('association_pk'))
        if self.object.is_online:
            raise Http404
        return super(AssociationDirectoryEntryPublishView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object.is_online = True
        self.object.save()
        return redirect(reverse('association-directory-detail', kwargs={
            'association_pk': self.association.id
        }))


class AssociationDirectoryEntryDeleteView(AssociationMixin, TemplateView):
    template_name = 'directory/delete.html'
    http_method_names = ['get', 'post']

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('directory.admin_directoryentry'):
            raise PermissionDenied
        return super(AssociationDirectoryEntryDeleteView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        DirectoryEntry.objects.all().filter(association_id=self.association.id).delete()
        return redirect(reverse('association-directory-detail', kwargs={
            'association_pk': self.association.id
        }))


class AssociationDirectoryPublicView(ListView):
    template_name = 'directory/public.html'
    model = Association
    context_object_name = 'associations'
    queryset = Association.objects.filter(is_active=True)
