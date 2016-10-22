from django.conf.urls import url

from portailva.association.views import AssociationDetailView, AssociationUpdateView, AssociationListView, \
    AssociationNewView, AssociationDeleteView, AssociationFileTreeView, AssociationFileUploadView

urlpatterns = [
    # Association links
    url('^new/$', AssociationNewView.as_view(), name='association-new'),
    url('^(?P<pk>\d+)/$', AssociationDetailView.as_view(), name='association-detail'),
    url('^(?P<pk>\d+)/update/$', AssociationUpdateView.as_view(), name='association-update'),

    # File
    url('^(?P<pk>\d+)/file(?:/(?P<folder_pk>\d+))?/$', AssociationFileTreeView.as_view(), name='association-file-tree'),
    url('^(?P<pk>\d+)/file/(?P<folder_pk>\d+)/upload/$', AssociationFileUploadView.as_view(), name='association-file-upload'),

    # Admin stuff
    url('^$', AssociationListView.as_view(), name='association-list'),
    url('^(?P<pk>\d+)/delete/$', AssociationDeleteView.as_view(), name='association-delete')
]