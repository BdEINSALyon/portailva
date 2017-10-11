from django.contrib import admin
from .models import Category, Association, Mandate, PeopleRole, People, Requirement, Accomplishment


@admin.register(Association)
class AssociationAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'acronym', 'category', 'active_members_number', 'is_active', 'is_validated', 'has_place'
    list_editable = 'acronym', 'category', 'active_members_number', 'is_active', 'is_validated', 'has_place'
    list_display_links = 'name',
    search_fields = 'name', 'acronym',
    list_filter = 'category', 'is_active', 'is_validated', 'has_place'
    ordering = 'name', 'id'


admin.site.register(Category)
admin.site.register(Mandate)
admin.site.register(PeopleRole)
admin.site.register(People)
admin.site.register(Requirement)
admin.site.register(Accomplishment)
