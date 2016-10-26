from django.contrib import admin

# Register your models here.
from portailva.file.models import File, FileVersion, AssociationFile, FileType, FileFolder

admin.site.register(File)
admin.site.register(FileType)
admin.site.register(FileVersion)
admin.site.register(AssociationFile)
admin.site.register(FileFolder)