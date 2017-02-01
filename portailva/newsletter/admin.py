from django.contrib import admin

# Register your models here.
from portailva.newsletter.models import Article, Newsletter

admin.site.register(Article)
admin.site.register(Newsletter)
