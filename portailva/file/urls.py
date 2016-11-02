from django.conf.urls import url

from .views import FileListView, FileView, AssociationFileTreeView, AssociationFileUploadView, AssociationFileDeleteView

urlpatterns = [
    # File
    url('^file/(?P<pk>\d+)/$', FileView.as_view(), name='file-view'),

    # Association file
    url('^association/(?P<association_pk>\d+)/file/tree(?:/(?P<folder_pk>\d+))?/$', AssociationFileTreeView.as_view(),
        name='association-file-tree'),
    url('^association/(?P<association_pk>\d+)/file/tree/(?P<folder_pk>\d+)/upload/$',
        AssociationFileUploadView.as_view(), name='association-file-upload'),
    url('^association/(?P<association_pk>\d+)/file/(?P<pk>\d+)/delete/$', AssociationFileDeleteView.as_view(),
        name='association-file-delete'),

    # Admin stuff
    url('^file/$', FileListView.as_view(), name='file-list'),
]
