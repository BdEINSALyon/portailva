from django.http import Http404

from portailva.association.mixins import AssociationMixin
from .models import DirectoryEntry, OpeningHour


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
