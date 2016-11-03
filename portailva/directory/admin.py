from django.contrib import admin

# Register your models here.
from portailva.directory.models import DirectoryEntry, OpeningHour

admin.site.register(DirectoryEntry)
admin.site.register(OpeningHour)
