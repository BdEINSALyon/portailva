from django.conf.urls import url

from portailva.file.views import ResourceFileListView, ResourceFileDeleteView, ResourceFileCreateView, \
    AssociationResourceFileTreeView, FileListView, FileView, AssociationFileTreeView, AssociationFileUploadView, \
    AssociationFileDeleteView, ResourceFolderListView, ResourceFolderDeleteView, ResourceFolderCreateView

urlpatterns = [
    # File
    url('^file/(?P<pk>\d+)/$', FileView.as_view(), name='file-view'),

    # Association file
    url('^association/(?P<association_pk>\d+)/file/tree(?:/(?P<folder_pk>\d+))?/$', AssociationFileTreeView.as_view(),
        name='association-file-tree'),
    url('^association/(?P<association_pk>\d+)/resources(?:/(?P<folder_pk>\d+))?/$', AssociationResourceFileTreeView.as_view(),
        name='resource-file-tree'),
    url('^association/(?P<association_pk>\d+)/file/tree/(?P<folder_pk>\d+)/upload/$',
        AssociationFileUploadView.as_view(), name='association-file-upload'),
    url('^association/(?P<association_pk>\d+)/file/(?P<pk>\d+)/delete/$', AssociationFileDeleteView.as_view(),
        name='association-file-delete'),

    # Admin stuff
    url('^file/$', FileListView.as_view(), name='file-list'),
    url('^resources/files/$', ResourceFileListView.as_view(), name='resource-file-list'),
    url('^resources/files/(?P<pk>\d+)/delete$', ResourceFileDeleteView.as_view(), name='resource-file-delete'),
    url('^resources/files/new$', ResourceFileCreateView.as_view(), name='resource-file-create'),
    url('^resources/folders/$', ResourceFolderListView.as_view(), name='resource-folder-list'),
    url('^resources/folders/(?P<pk>\d+)/delete$', ResourceFolderDeleteView.as_view(), name='resource-folder-delete'),
    url('^resources/folders/new$', ResourceFolderCreateView.as_view(), name='resource-folder-create'),
]
