from django.contrib import admin

# Register your models here.
from portailva.event.models import EventType, Event, EventPrice

admin.site.register(EventType)
admin.site.register(Event)
admin.site.register(EventPrice)
