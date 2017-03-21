from portailva.file.views.admin_files import FileListView
from portailva.file.views.admin_resource_files import ResourceFileListView, ResourceFileDeleteView, \
    ResourceFileCreateView
from portailva.file.views.association_files_management import AssociationFileTreeView, AssociationFileUploadView, \
    AssociationFileDeleteView, AssociationResourceFileTreeView
from portailva.file.views.files import FileView

__all__ = [
    'FileListView', 'FileView', 'AssociationFileTreeView', 'AssociationFileUploadView', 'AssociationFileDeleteView',
    'ResourceFileListView', 'ResourceFileDeleteView', 'ResourceFileCreateView', 'AssociationResourceFileTreeView'
]
