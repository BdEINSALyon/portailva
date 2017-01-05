from django.contrib import admin

# Register your models here.
from portailva.newsletter.models import Article, ArticleNewsletterElement, EventNewsletterElement, Newsletter

admin.site.register(Article)
admin.site.register(ArticleNewsletterElement)
admin.site.register(EventNewsletterElement)
admin.site.register(Newsletter)
