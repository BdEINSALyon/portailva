from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

from portailva.association.models import Association
from portailva.event.models import Event


class Article(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    association = models.ForeignKey(Association, related_name='articles', verbose_name='Association')
    validated = models.BooleanField(verbose_name='publié', default=False)

    title = models.CharField(max_length=255, verbose_name="Titre")
    short_content = models.CharField(max_length=255, verbose_name="Description courte")
    featured_image = models.ImageField(verbose_name="Image à la une", help_text="Cette image est utilisée dans "
                                                                                "l'envoie de la newsletter VA",
                                       blank=True, null=True)
    content = RichTextField(verbose_name="Contenu", blank=True, null=True)

    type = models.CharField(max_length=20, verbose_name="type", blank=False, default='CLASSIC',
                            choices=(('FEATURED', 'A la une'), ('CLASSIC', 'Normal')))

    def __str__(self):
        return "{} - {}".format(self.association.name, self.title)

    def can_update(self, user):
        if not user.has_perm('article.admin_article'):
            if user not in self.association.users.all():
                return False
            elif self.validated:
                return False
            else:
                return True
        else:
            return not self.validated

    def can_delete(self, user):
        if not user.has_perm('article.admin_article'):
            if user not in self.association.users.all():
                return False
            elif self.validated:
                return False
            else:
                return True
        else:
            return True


class Newsletter(models.Model):

    title = models.CharField(max_length=255, verbose_name='Nom')
    sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    articles = models.ManyToManyField(Article, related_name='newsletter', verbose_name='Articles')
    events = models.ManyToManyField(Event, related_name='newsletter', verbose_name='Evènements')

    def __str__(self):
        return "{}".format(self.title)
