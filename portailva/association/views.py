from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from django.views.generic.detail import SingleObjectMixin

from portailva.association.forms import AssociationForm, AssociationAdminForm, AssociationFileUploadForm, MandateForm, \
    PeopleForm, DirectoryEntryForm, OpeningHourForm
from portailva.association.models import Association, Mandate, People, DirectoryEntry, OpeningHour
from portailva.file.models import AssociationFile, FileFolder, FileVersion


class AssociationListView(ListView):
    template_name = 'association/list.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        if not request.user.has_perm('association.admin_association'):
            raise PermissionDenied
        return super(AssociationListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Association.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AssociationListView, self).get_context_data(**kwargs)
        return context


class AssociationDetailView(DetailView):
    model = Association
    template_name = 'association/detail.html'
    object = None

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.can_access(request.user):
            raise PermissionDenied
        return super(AssociationDetailView, self).get(request, *args, **kwargs)


class AssociationMixin(object):
    association = None

    @method_decorator(login_required)
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


class AssociationUpdateView(UpdateView):
    template_name = 'association/update.html'
    form_class = AssociationForm
    model = Association
    object = None

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.can_access(request.user):
            raise PermissionDenied
        if self.object.can_admin(request.user):
            self.form_class = AssociationAdminForm
        return super(AssociationUpdateView, self).dispatch(request, *args, **kwargs)

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form = self.create_form(self.form_class, **{
            'name': self.object.name,
            'category': self.object.category,
            'acronym': self.object.acronym,
            'description': self.object.description,
            'is_active': self.object.is_active
        })

        return render(request, self.template_name, {'association': self.object, 'form': form})

    @method_decorator(login_required)
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
        self.object.category_id = form.data.get('category')
        self.object.acronym = form.data.get('acronym')
        self.object.description = form.data.get('description')

        # Admin form
        if self.form_class is AssociationAdminForm:
            self.object.is_active = False if not form.data.get('is_active') else True

        self.object.save()

        messages.add_message(self.request, messages.SUCCESS, "Les informations ont bien été mises à jour.")

        return redirect(reverse('association-detail', kwargs={'pk': self.object.id}))


class AssociationNewView(CreateView):
    template_name = 'association/new.html'
    form_class = AssociationAdminForm

    def get_form(self, form_class=AssociationAdminForm):
        return form_class(self.request.POST)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'form': self.form_class()})

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.form_class)

        if form.is_valid():
            return self.form_valid(form)
        return render(request, self.template_name, {'form': form})

    def form_valid(self, form):
        association = Association()
        association.name = form.data.get('name')
        association.category_id = form.data.get('category')
        association.acronym = form.data.get('acronym')
        association.description = form.data.get('description')
        association.is_active = True if form.data.get('is_active') else False
        association.save()

        return redirect(reverse('association-list'))


class AssociationDeleteView(DeleteView):
    model = Association
    template_name = 'association/delete.html'
    success_url = reverse_lazy('association-list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.can_admin(request.user):
            raise PermissionDenied
        return super(AssociationDeleteView, self).dispatch(request, *args, **kwargs)


# File
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


# Mandates
class AssociationMandateListView(AssociationMixin, ListView):
    model = Mandate
    template_name = 'association/mandate/list.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        if not request.user.has_perm('association.can_admin_mandate'):
            raise PermissionDenied
        return super(AssociationMandateListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AssociationMandateListView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Mandate.objects.all()\
            .prefetch_related('peoples')\
            .prefetch_related('peoples__role')\
            .filter(association_id=self.association.id)\
            .order_by('-begins_at')


class AssociationMandateNewView(AssociationMixin, CreateView):
    model = Mandate
    form_class = MandateForm
    template_name = 'association/mandate/new.html'

    def get_form(self, form_class=MandateForm):
        return form_class(self.request.POST, association=self.association)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'form': self.form_class(association=self.association),
            'association': self.association
        })

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.form_class)

        if form.is_valid():
            return self.form_valid(form)
        return render(request, self.template_name, {
            'form': form,
            'association': self.association
        })

    def form_valid(self, form):
        Mandate.objects.create(
            begins_at=form.cleaned_data.get('begins_at'),
            ends_at=form.cleaned_data.get('ends_at'),
            association_id=self.association.id
        )

        return redirect(reverse('association-mandate-list', kwargs={
            'association_pk': self.association.id
        }))


class AssociationMandateMixin(AssociationMixin):
    mandate = None
    success_url = None

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        mandate = Mandate.objects.all()\
            .filter(association_id=kwargs.get('association_pk'))\
            .order_by('-begins_at')[:1]
        if len(mandate) < 1:
            raise Http404
        if mandate[0].id != int(kwargs.get('mandate_pk', None)):
            raise Http404
        self.mandate = mandate[0]
        self.success_url = reverse('association-mandate-list', kwargs={
            'association_pk': kwargs.get('association_pk')
        })
        return super(AssociationMandateMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AssociationMandateMixin, self).get_context_data(**kwargs)
        context['mandate'] = self.mandate
        return context


class AssociationMandatePeopleNewView(AssociationMandateMixin, CreateView):
    model = People
    form_class = PeopleForm
    template_name = 'association/mandate/people_new.html'

    def form_valid(self, form):
        people = form.save(commit=False)
        people.mandate = self.mandate
        people.save()
        return redirect(reverse('association-mandate-list', kwargs={
            'association_pk': self.association.id
        }))


class AssociationMandatePeopleMixin(AssociationMandateMixin):
    def get_object(self, queryset=None):
        try:
            # We make sure mandate_pk provided in url matches with mandate linked to people
            people = People.objects.get(id=self.kwargs.get('pk', None))
            if people.mandate_id != self.mandate.id:
                raise Http404
        except People.DoesNotExist:
            raise Http404
        return people


class AssociationMandatePeopleUpdateView(AssociationMandatePeopleMixin, UpdateView):
    model = People
    form_class = PeopleForm
    template_name = 'association/mandate/people_edit.html'


class AssociationMandatePeopleDeleteView(AssociationMandateMixin, DeleteView):
    model = People
    template_name = 'association/mandate/people_delete.html'


# Directory
class AssociationDirectoryEntryMixin(AssociationMixin):
    object = None

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(AssociationDirectoryEntryMixin, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        try:
            return DirectoryEntry.objects.get_last_for_association_id(self.kwargs.get('association_pk'))
        except IndexError:
            return None

    def get_context_data(self, **kwargs):
        context = super(AssociationDirectoryEntryMixin, self).get_context_data(**kwargs)
        context['days'] = OpeningHour.DAYS_OF_WEEK
        return context


class AssociationDirectoryEntryDetailView(AssociationDirectoryEntryMixin, DetailView):
    model = DirectoryEntry
    template_name = 'association/directory_entry/detail.html'


class AssociationDirectoryEntryUpdateView(AssociationDirectoryEntryMixin, UpdateView):
    model = DirectoryEntry
    form_class = DirectoryEntryForm
    template_name = 'association/directory_entry/update.html'

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
    template_name = 'association/directory_entry/opening_hour_new.html'

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


class OpeningHourMixin(AssociationMixin):
    def get_object(self, queryset=None):
        try:
            opening_hour = OpeningHour.objects.get(pk=self.kwargs.get('pk'))
            # We ensure association_pk provided matches association linked with opening hour
            if opening_hour.directory_entry.association_id != int(self.kwargs.get('association_pk')):
                raise Http404

            # We ensure opening hour user wants to get belongs to last directory entry
            if opening_hour.directory_entry_id != DirectoryEntry.objects\
                    .get_last_for_association_id(self.kwargs.get('association_pk')).id:
                raise Http404
        except OpeningHour.DoesNotExist:
            raise Http404
        return opening_hour

    def get_context_data(self, **kwargs):
        context = super(OpeningHourMixin, self).get_context_data(**kwargs)
        context['days'] = OpeningHour.DAYS_OF_WEEK
        return context


class AssociationDirectoryEntryOpeningHourUpdateView(OpeningHourMixin, UpdateView):
    form_class = OpeningHourForm
    template_name = 'association/directory_entry/opening_hour_update.html'
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
    template_name = 'association/directory_entry/opening_hour_delete.html'
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
    template_name = 'association/directory_entry/publish.html'
    http_method_names = ['get', 'post']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('association.admin_directoryentry'):
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
    template_name = 'association/directory_entry/delete.html'
    http_method_names = ['get', 'post']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('association.admin_directoryentry'):
            raise PermissionDenied
        return super(AssociationDirectoryEntryDeleteView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        DirectoryEntry.objects.all().filter(association_id=self.association.id).delete()
        return redirect(reverse('association-directory-detail', kwargs={
            'association_pk': self.association.id
        }))
