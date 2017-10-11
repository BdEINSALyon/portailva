from itertools import groupby

from django.db import models

from portailva.association.models import Association
from portailva.utils.models import Place


class DirectoryEntryManager(models.Manager):
    def get_last_for_association_id(self, association_id):
        return self.get_queryset()\
            .filter(association_id=association_id)\
            .order_by('-id')[:1][0]

    def get_last_active(self):
        return [list(g)[0] for k, g in groupby(DirectoryEntry.objects.all().filter(is_online=True)
                                               .order_by('association__name', '-created_at'), lambda x: x.association_id)]


class DirectoryEntry(models.Model):
    """
    A DirectoryEntry contains useful information about an Association.
    It contains address and some contact information.
    """
    description = models.TextField("Description de l'association")
    contact_address = models.EmailField("Adresse de contact")
    phone = models.CharField("Téléphone", max_length=10, blank=True, null=True)

    website_url = models.URLField("URL site web", null=True, blank=True)
    facebook_url = models.URLField("URL page Facebook", null=True, blank=True)
    twitter_url = models.URLField("URL fil Twitter", null=True, blank=True)

    association = models.ForeignKey(Association, verbose_name="Association", related_name="directory_entries",
                                    on_delete=models.CASCADE)
    place = models.ForeignKey(Place, verbose_name="Lieu", related_name="associations", null=True, blank=True,
                              on_delete=models.SET_NULL)

    is_online = models.BooleanField("Est publié", default=False)

    created_at = models.DateTimeField("Date d'ajout", auto_now_add=True)
    updated_at = models.DateTimeField("Dernière mise à jour", auto_now=True)

    objects = DirectoryEntryManager()

    class Meta(object):
        default_permissions = ('add', 'change', 'delete', 'admin',)

    def __str__(self):
        return "[" + self.association.name + "] Version du " + str(self.created_at)


class OpeningHour(models.Model):
    """
    An OpeningHour is a time range when association welcomes visitors.
    """
    DAYS_OF_WEEK = (
        (1, 'Lundi'),
        (2, 'Mardi'),
        (3, 'Mercredi'),
        (4, 'Jeudi'),
        (5, 'Vendredi'),
        (6, 'Samedi'),
        (7, 'Dimanche'),
    )
    day = models.IntegerField("Jour d'ouverture", choices=DAYS_OF_WEEK)
    begins_at = models.TimeField("Heure d'ouverture")
    ends_at = models.TimeField("Heure de fermeture")

    directory_entry = models.ForeignKey(DirectoryEntry, verbose_name="Version du Bot'INSA",
                                        related_name="opening_hours", on_delete=models.CASCADE)

    class Meta(object):
        default_permissions = ('add', 'change', 'delete', 'admin',)
        ordering = ('day', 'begins_at', )

    def __str__(self):
        return "[" + self.directory_entry.association.name + "] " + self.get_day_display() + " de " +\
               str(self.begins_at) + " à " + str(self.ends_at) + " - Version du " +\
               str(self.directory_entry.created_at)
