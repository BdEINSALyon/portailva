from django.conf.urls import url

from .views import AssociationEventListView, AssociationEventNewView, AssociationEventUpdateView, \
    AssociationEventDetailView, AssociationEventDeleteView, AssociationEventPriceNewView, \
    AssociationEventPriceUpdateView, AssociationEventPriceDeleteView, AssociationEventPublishView, EventDetailView, \
    AllEventsCalendarView

urlpatterns = [
    url('^events/(?P<pk>\d+)$',
        EventDetailView.as_view(), name='event-about'),
    url('^events/calendar$',
        AllEventsCalendarView.as_view(), name='event-calendar'),
    url('^association/(?P<association_pk>\d+)/event/$', AssociationEventListView.as_view(),
        name='association-event-list'),
    url('^association/(?P<association_pk>\d+)/event/new/$', AssociationEventNewView.as_view(),
        name='association-event-new'),
    url('^association/(?P<association_pk>\d+)/event/(?P<pk>\d+)/$', AssociationEventDetailView.as_view(),
        name='association-event-detail'),
    url('^association/(?P<association_pk>\d+)/event/(?P<pk>\d+)/update/$', AssociationEventUpdateView.as_view(),
        name='association-event-update'),
    url('^association/(?P<association_pk>\d+)/event/(?P<pk>\d+)/delete/$', AssociationEventDeleteView.as_view(),
        name='association-event-delete'),
    url('^association/(?P<association_pk>\d+)/event/(?P<event_pk>\d+)/price/new/$',
        AssociationEventPriceNewView.as_view(), name='association-event-price-new'),
    url('^association/(?P<association_pk>\d+)/event/(?P<event_pk>\d+)/price/(?P<pk>\d+)/update/$',
        AssociationEventPriceUpdateView.as_view(), name='association-event-price-update'),
    url('^association/(?P<association_pk>\d+)/event/(?P<event_pk>\d+)/price/(?P<pk>\d+)/delete/$',
        AssociationEventPriceDeleteView.as_view(), name='association-event-price-delete'),

    # Admin stuff
    url('^association/(?P<association_pk>\d+)/event/(?P<event_pk>\d+)/publish/$',
        AssociationEventPublishView.as_view(), name='association-event-publish')
]
