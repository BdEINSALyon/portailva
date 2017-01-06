from django.db import models

from portailva.association.models import Association
from portailva.event.models import Event


class Article(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    association = models.ForeignKey(Association, related_name='articles', verbose_name='Association')
    validated = models.BooleanField(verbose_name='publié', default=False)

    title = models.CharField(max_length=255, verbose_name="Titre")
    content = models.TextField(verbose_name="contenu")

    type = models.CharField(max_length=20, verbose_name="type",
                            choices=(('FEATURED', 'A la une'), ('CLASSIC', 'Normal')))

    def __str__(self):
        return "{} - {}".format(self.association.name, self.title)

    def can_update(self, user):
        if not user.has_perm('article.admin_article'):
            if user not in self.association.users.all():
                return False
            elif self.is_online:
                return False
            else:
                return True
        else:
            return True

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


class NewsletterElement(models.Model):

    class Meta:
        abstract = True
        verbose_name = "Element de Newsletter"

    position = models.IntegerField(verbose_name='position')


class ArticleNewsletterElement(NewsletterElement):

    class Meta:
        verbose_name = "Article de newsletter"

    article = models.ForeignKey(Article, on_delete=models.CASCADE)


class EventNewsletterElement(NewsletterElement):

    class Meta:
        verbose_name = "Evenement de newsletter"

    event = models.ForeignKey(Event, on_delete=models.CASCADE)


class Newsletter(models.Model):

    title = models.CharField(max_length=255, verbose_name='Nom')
    sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    articles = models.ManyToManyField(ArticleNewsletterElement, related_name='newletter', verbose_name='Articles')
    events = models.ManyToManyField(EventNewsletterElement, related_name='newletter', verbose_name='Evènements')

    def __str__(self):
        return "{}".format(self.title)
