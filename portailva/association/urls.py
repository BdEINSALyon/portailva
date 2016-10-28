from django.conf.urls import url

from portailva.association.views import AssociationDetailView, AssociationUpdateView, AssociationListView, \
    AssociationNewView, AssociationDeleteView, AssociationFileTreeView, AssociationFileUploadView, \
    AssociationFileDeleteView, AssociationMandateListView, AssociationMandateNewView, AssociationMandatePeopleNewView, \
    AssociationMandatePeopleUpdateView, AssociationMandatePeopleDeleteView, AssociationDirectoryEntryDetailView, \
    AssociationDirectoryEntryUpdateView, AssociationDirectoryEntryOpeningHourCreateView, \
    AssociationDirectoryEntryOpeningHourUpdateView, AssociationDirectoryEntryOpeningHourDeleteView, \
    AssociationDirectoryEntryPublishView, AssociationDirectoryEntryDeleteView

urlpatterns = [
    # Association links
    url('^new/$', AssociationNewView.as_view(), name='association-new'),
    url('^(?P<pk>\d+)/$', AssociationDetailView.as_view(), name='association-detail'),
    url('^(?P<pk>\d+)/update/$', AssociationUpdateView.as_view(), name='association-update'),

    # File
    url('^(?P<association_pk>\d+)/file/tree(?:/(?P<folder_pk>\d+))?/$', AssociationFileTreeView.as_view(),
        name='association-file-tree'),
    url('^(?P<association_pk>\d+)/file/tree/(?P<folder_pk>\d+)/upload/$', AssociationFileUploadView.as_view(),
        name='association-file-upload'),
    url('^(?P<association_pk>\d+)/file/(?P<pk>\d+)/delete/$', AssociationFileDeleteView.as_view(),
        name='association-file-delete'),

    # Mandate
    url('^(?P<association_pk>\d+)/mandate/$', AssociationMandateListView.as_view(), name='association-mandate-list'),
    url('^(?P<association_pk>\d+)/mandate/new/$', AssociationMandateNewView.as_view(), name='association-mandate-new'),
    url('^(?P<association_pk>\d+)/mandate/(?P<mandate_pk>\d+)/people/new/$', AssociationMandatePeopleNewView.as_view(),
        name='association-mandate-people-new'),
    url('^(?P<association_pk>\d+)/mandate/(?P<mandate_pk>\d+)/people/(?P<pk>\d+)/edit/$',
        AssociationMandatePeopleUpdateView.as_view(), name='association-mandate-people-update'),
    url('^(?P<association_pk>\d+)/mandate/(?P<mandate_pk>\d+)/people/(?P<pk>\d+)/delete/$',
        AssociationMandatePeopleDeleteView.as_view(), name='association-mandate-people-delete'),

    # Directory entry
    url('^(?P<association_pk>\d+)/directory/$', AssociationDirectoryEntryDetailView.as_view(),
        name='association-directory-detail'),
    url('^(?P<association_pk>\d+)/directory/edit/$', AssociationDirectoryEntryUpdateView.as_view(),
        name='association-directory-update'),
    url('^(?P<association_pk>\d+)/directory/opening_hour/new/$', AssociationDirectoryEntryOpeningHourCreateView
        .as_view(), name='association-directory-opening-hour-new'),
    url('^(?P<association_pk>\d+)/directory/opening_hour/(?P<pk>\d+)/update/$',
        AssociationDirectoryEntryOpeningHourUpdateView.as_view(), name='association-directory-opening-hour-update'),
    url('^(?P<association_pk>\d+)/directory/opening_hour/(?P<pk>\d+)/delete/$',
        AssociationDirectoryEntryOpeningHourDeleteView.as_view(), name='association-directory-opening-hour-delete'),

    # Admin stuff
    url('^$', AssociationListView.as_view(), name='association-list'),
    url('^(?P<pk>\d+)/delete/$', AssociationDeleteView.as_view(), name='association-delete'),
    url('^(?P<association_pk>\d+)/directory/publish/$', AssociationDirectoryEntryPublishView.as_view(),
        name='association-directory-publish'),
    url('^(?P<association_pk>\d+)/directory/delete/$', AssociationDirectoryEntryDeleteView.as_view(),
        name='association-directory-delete')

]