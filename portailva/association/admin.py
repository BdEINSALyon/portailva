from django.contrib import admin
from .models import Category, Association, Mandate, PeopleRole, People

# Register your models here.
admin.site.register(Association)
admin.site.register(Category)
admin.site.register(Mandate)
admin.site.register(PeopleRole)
admin.site.register(People)
