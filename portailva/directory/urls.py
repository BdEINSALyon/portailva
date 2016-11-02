from django.conf.urls import url

from .views import AssociationDirectoryEntryDetailView, AssociationDirectoryEntryUpdateView, \
    AssociationDirectoryEntryOpeningHourCreateView, AssociationDirectoryEntryOpeningHourUpdateView, \
    AssociationDirectoryEntryOpeningHourDeleteView, AssociationDirectoryEntryPublishView, \
    AssociationDirectoryEntryDeleteView

urlpatterns = [
    url('^association/(?P<association_pk>\d+)/directory/$', AssociationDirectoryEntryDetailView.as_view(),
        name='association-directory-detail'),
    url('^association/(?P<association_pk>\d+)/directory/edit/$', AssociationDirectoryEntryUpdateView.as_view(),
        name='association-directory-update'),
    url('^association/(?P<association_pk>\d+)/directory/opening_hour/new/$', AssociationDirectoryEntryOpeningHourCreateView
        .as_view(), name='association-directory-opening-hour-new'),
    url('^association/(?P<association_pk>\d+)/directory/opening_hour/(?P<pk>\d+)/update/$',
        AssociationDirectoryEntryOpeningHourUpdateView.as_view(), name='association-directory-opening-hour-update'),
    url('^association/(?P<association_pk>\d+)/directory/opening_hour/(?P<pk>\d+)/delete/$',
        AssociationDirectoryEntryOpeningHourDeleteView.as_view(), name='association-directory-opening-hour-delete'),

    # Admin stuff
    url('^association/(?P<association_pk>\d+)/directory/publish/$', AssociationDirectoryEntryPublishView.as_view(),
        name='association-directory-publish'),
    url('^association/(?P<association_pk>\d+)/directory/delete/$', AssociationDirectoryEntryDeleteView.as_view(),
        name='association-directory-delete')
]
