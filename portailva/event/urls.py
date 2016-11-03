from django.conf.urls import url

from .views import AssociationEventListView, AssociationEventNewView, AssociationEventUpdateView, \
    AssociationEventDetailView, AssociationEventDeleteView

urlpatterns = [
    url('^association/(?P<association_pk>\d+)/event/$', AssociationEventListView.as_view(),
        name='association-event-list'),
    url('^association/(?P<association_pk>\d+)/event/new/$', AssociationEventNewView.as_view(),
        name='association-event-new'),
    url('^association/(?P<association_pk>\d+)/event/(?P<pk>\d+)/$', AssociationEventDetailView.as_view(),
        name='association-event-detail'),
    url('^association/(?P<association_pk>\d+)/event/(?P<pk>\d+)/update/$', AssociationEventUpdateView.as_view(),
        name='association-event-update'),
    url('^association/(?P<association_pk>\d+)/event/(?P<pk>\d+)/delete/$', AssociationEventDeleteView.as_view(),
        name='association-event-delete')

    # Admin stuff
]
