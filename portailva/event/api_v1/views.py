import datetime

from django.db.models import Q
from rest_framework.exceptions import ParseError
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from portailva.event.api_v1.serializers import EventSerializer
from portailva.event.models import Event


class EventListAPIView(ListAPIView):
    serializer_class = EventSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        queryset = Event.objects.get_online()
        since = self.request.query_params.get('since', None)
        until = self.request.query_params.get('until', None)

        if since is None and until is None:
            # We return event for the next two days
            since = datetime.datetime.now().strftime('%Y-%m-%d')
            until = (datetime.datetime.now() + datetime.timedelta(days=7)).strftime('%Y-%m-%d')

        if since is not None and until is None:
            try:
                since_date = datetime.datetime.strptime(since, '%Y-%m-%d')
                queryset = queryset.filter(
                    (Q(begins_at__lte=since_date) & Q(begins_at__gte=since_date)) |
                    (Q(begins_at__gte=since_date))
                )
            except ValueError:
                raise ParseError("Bad format for since parameter. Accepted format : %Y-%m-%d.")
        elif since is None and until is not None:
            try:
                until_date = datetime.datetime.strptime(until, '%Y-%m-%d')
                queryset = queryset.filter(
                    (Q(begins_at__lte=until_date) & Q(ends_at__gte=until_date)) |
                    (Q(ends_at__lte=until_date))
                )
            except ValueError:
                raise ParseError("Bad format for until parameter. Accepted format : %Y-%m-%d.")
        else:
            try:
                since_date = datetime.datetime.strptime(since, '%Y-%m-%d')
                until_date = datetime.datetime.strptime(until, '%Y-%m-%d')
                queryset = queryset.filter(
                    (Q(begins_at__gte=since_date) & Q(begins_at__lte=until_date)) |
                    (Q(ends_at__gte=since_date) & Q(ends_at__lte=until_date)) |
                    (Q(begins_at__lte=since_date) & Q(ends_at__gte=until_date))
                )
            except ValueError:
                raise ParseError("Bad format for since/until parameters. Accepted format : %Y-%m-%d.")
        return queryset
