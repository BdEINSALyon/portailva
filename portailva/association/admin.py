from django.contrib import admin
from .models import Category, Association

# Register your models here.
admin.site.register(Association)
admin.site.register(Category)
