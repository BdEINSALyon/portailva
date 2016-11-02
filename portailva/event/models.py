from django.db import models

from portailva.association.models import Association
from portailva.file.models import File
from portailva.utils.models import Place


class EventType(models.Model):
    name = models.CharField("Nom", max_length=50)

    class Meta(object):
        default_permissions = ('add', 'change', 'delete', 'admin',)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField("Nom", max_length=50)
    short_description = models.TextField("Description courte", max_length=150)
    description = models.TextField("Description")

    is_online = models.BooleanField("Est publié", default=False)

    type = models.ForeignKey(EventType, verbose_name="Type d'événement", related_name="events", null=True,
                             on_delete=models.SET_NULL)
    association = models.ForeignKey(Association, verbose_name="Association", related_name="events",
                                    on_delete=models.CASCADE)
    place = models.ForeignKey(Place, verbose_name="Lieu", related_name="events", null=True, on_delete=models.SET_NULL)
    picture = models.ForeignKey(File, verbose_name="Image", blank=True, null=True, on_delete=models.SET_NULL)

    begins_at = models.DateTimeField("Date de début")
    ends_at = models.DateTimeField("Date de fin")
    created_at = models.DateTimeField("Date d'ajout", auto_now_add=True)
    updated_at = models.DateTimeField("Dernière mise à jour", auto_now=True)

    class Meta(object):
        default_permissions = ('add', 'change', 'delete', 'admin',)

    def __str__(self):
        return self.name


class EventPrice(models.Model):
    name = models.CharField("Nom du tarif", max_length=50)
    price = models.DecimalField("Tarif", max_digits=8, decimal_places=2)

    event = models.ForeignKey(Event, verbose_name="Evénement", related_name="prices", on_delete=models.CASCADE)

    is_va = models.BooleanField("Est un tarif VA ?", default=False)
    is_variable = models.BooleanField("Prix libre ?", default=False)

    class Meta(object):
        default_permissions = ('add', 'change', 'delete', 'admin',)

    def __str__(self):
        return '[' + self.event.name + '] ' + self.name
