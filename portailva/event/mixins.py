from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse

from portailva.association.mixins import AssociationMixin
from portailva.event.models import Event


class AssociationEventMixin(AssociationMixin):
    event = None

    def dispatch(self, request, *args, **kwargs):
        self.event = get_object_or_404(Event, pk=kwargs.get('event_pk', None))
        if self.event.association_id != int(kwargs.get('association_pk', 0)):
            raise Http404
        return super(AssociationEventMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AssociationEventMixin, self).get_context_data(**kwargs)
        context.update({
            'event': self.event
        })
        return context


class AssociationEventPriceMixin(AssociationEventMixin):
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.event_id != int(kwargs.get('event_pk', 0)):
            raise Http404
        return super(AssociationEventPriceMixin, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if not self.event.can_update(request.user):
            raise Http404
        return super(AssociationEventPriceMixin, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not self.event.can_update(request.user):
            raise Http404
        return super(AssociationEventPriceMixin, self).post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(AssociationEventPriceMixin, self).get_form_kwargs()
        kwargs.update({
            'event': self.event
        })

        return kwargs

    def get_success_url(self):
        return reverse('association-event-detail', kwargs={
            'association_pk': self.association.id,
            'pk': self.event.id
        })
