from django.conf.urls import url

from .views import AssociationEventListView, AssociationEventNewView, AssociationEventUpdateView

urlpatterns = [
    url('^association/(?P<association_pk>\d+)/event/$', AssociationEventListView.as_view(),
        name='association-event-list'),
    url('^association/(?P<association_pk>\d+)/event/new/$', AssociationEventNewView.as_view(),
        name='association-event-new'),
    url('^association/(?P<association_pk>\d+)/event/(?P<pk>\d+)/$', AssociationEventUpdateView.as_view(),
        name='association-event-update'),

    # Admin stuff
]
