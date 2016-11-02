from django.conf.urls import url

from .views import AssociationEventListView, AssociationEventNewView

urlpatterns = [
    url('^association/(?P<association_pk>\d+)/event/$', AssociationEventListView.as_view(),
        name='association-event-list'),
    url('^association/(?P<association_pk>\d+)/event/new/$', AssociationEventNewView.as_view(),
        name='association-event-new')

    # Admin stuff
]
