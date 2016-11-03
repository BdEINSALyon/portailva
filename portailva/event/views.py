from datetime import datetime

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from portailva.association.mixins import AssociationMixin
from portailva.event.forms import EventForm
from .models import Event


class AssociationEventListView(AssociationMixin, ListView):
    model = Event
    template_name = 'event/association_event_list.html'

    def get_context_data(self, **kwargs):
        context = super(AssociationEventListView, self).get_context_data(**kwargs)
        context.update({
            'past_events': self.get_past_events()
        })
        return context

    def get_queryset(self):
        return Event.objects.all()\
            .select_related('type')\
            .filter(association_id=self.association.id)\
            .filter(ends_at__gte=datetime.now())\
            .order_by('begins_at')

    def get_past_events(self):
        return Event.objects.all()\
            .select_related('type')\
            .filter(association_id=self.association.id)\
            .filter(ends_at__lt=datetime.now())\
            .order_by('-ends_at')


class AssociationEventDetailView(AssociationMixin, DetailView):
    model = Event
    template_name = 'event/detail.html'

    def get_context_data(self, **kwargs):
        context = super(AssociationEventDetailView, self).get_context_data()
        context.update({
            'can_update': self.object.can_update(self.request.user),
            'can_delete': self.object.can_delete(self.request.user)
        })
        return context


class AssociationEventNewView(AssociationMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'event/new.html'

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse('association-event-list', kwargs={
            'association_pk': kwargs.get('association_pk')
        })
        return super(AssociationEventNewView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(AssociationEventNewView, self).get_form_kwargs()
        kwargs.update({
            'association': self.association
        })

        return kwargs


class AssociationEventUpdateView(AssociationMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'event/update.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Can't update event after its validation
        if not self.object.can_update(request.user):
            raise PermissionDenied
        self.success_url = reverse('association-event-list', kwargs={
            'association_pk': kwargs.get('association_pk')
        })
        return super(AssociationEventUpdateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(AssociationEventUpdateView, self).get_form_kwargs()
        kwargs.update({
            'association': self.association
        })

        return kwargs


class AssociationEventDeleteView(AssociationMixin, DeleteView):
    model = Event
    template_name = 'event/delete.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.can_delete(request.user):
            raise PermissionDenied
        self.success_url = reverse('association-event-list', kwargs={
            'association_pk': kwargs.get('association_pk')
        })
        return super(AssociationEventDeleteView, self).dispatch(request, *args, **kwargs)
