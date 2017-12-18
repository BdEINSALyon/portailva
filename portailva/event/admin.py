from django.contrib import admin

# Register your models here.
from portailva.event.models import EventType, Event, EventPrice


def publish(modeladmin, request, queryset):
    queryset.update(is_online=True)


publish.short_description = "Publier les évènements sélectionnés"


class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_online', 'type', 'begins_at', 'ends_at']
    ordering = ['name']
    actions = [publish]


admin.site.register(EventType)
admin.site.register(Event, EventAdmin)
admin.site.register(EventPrice)
