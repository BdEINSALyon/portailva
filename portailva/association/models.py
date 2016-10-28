from django.db import models
from django.contrib.auth.models import User


# Create your models here.
from portailva.utils.models import Place


class Category(models.Model):
    """
    A Category is a simple container for Associations.
    There is no kind of logic in a Category. It simply here for Association presentation in a predefined order.
    """
    name = models.CharField("Nom", max_length=50)
    position = models.IntegerField("Position", blank=True)

    class Meta(object):
        default_permissions = ('add', 'change', 'delete', 'admin',)

    def __str__(self):
        return self.name


class Association(models.Model):
    """
    An Association.
    """
    name = models.CharField("Nom", max_length=50)
    acronym = models.CharField("Acronyme", max_length=20, null=True, blank=True)
    description = models.TextField("Description")

    is_active = models.BooleanField("Est active", default=True)
    is_validated = models.BooleanField("Est validée", default=False)
    has_place = models.BooleanField("Possède un local?", default=False)

    category = models.ForeignKey(Category, verbose_name="Catégorie")
    users = models.ManyToManyField(User, verbose_name="Utilisateurs", related_name='associations', blank=True)

    created_at = models.DateTimeField("Date d'ajout", auto_now_add=True)
    updated_at = models.DateTimeField("Dernière mise à jour", auto_now=True)

    class Meta(object):
        default_permissions = ('add', 'change', 'delete', 'admin',)

    def __str__(self):
        return self.name

    def can_admin(self, user):
        """
        Checks if an user can administrate an association.
        The association can be administrated if:
        - The user is an admin
        :param user: the user to check the rights
        :return: `True` if the user can access this association, `False` otherwise.
        """
        if user is not None and user.is_authenticated():
            if user.is_superuser or user.has_perm('association.admin_association'):
                return True

        return False

    def can_access(self, user):
        """
        Checks if an user can access information about an association.
        The association can be accessed if:
        - The user belongs to association users list
        - The user is an admin
        :param user: the user to check the rights
        :return: `True` if the user can access this association, `False` otherwise.
        """
        if user is not None and user.is_authenticated():
            if self.can_admin(user):
                return True
            elif user in self.users.all():
                return True

        return False


class Mandate(models.Model):
    """
    A Mandate is an Association period of activity. During a Mandate, some people manage the Association (like the
    president or the treasurer).
    """
    begins_at = models.DateField("Début du mandat")
    ends_at = models.DateField("Fin du mandat")
    created_at = models.DateTimeField("Date d'ajout", auto_now_add=True)

    association = models.ForeignKey(Association, verbose_name="Association", related_name="mandates",
                                    on_delete=models.CASCADE)

    class Meta(object):
        default_permissions = ('add', 'change', 'delete', 'admin',)

    def __str__(self):
        return "Du " + str(self.begins_at) + " au " + str(self.ends_at)


class PeopleRole(models.Model):
    """
    During a Mandate, each People has a specific PeopleRole.
    """
    name = models.CharField("Nom du poste", max_length=50)
    position = models.IntegerField("Position", blank=True, default=1)

    class Meta(object):
        default_permissions = ('add', 'change', 'delete', 'admin',)

    def __str__(self):
        return self.name


class People(models.Model):
    """
    A People designates someone who manages the Association during a Mandate.
    """
    first_name = models.CharField("Prénom", max_length=50)
    last_name = models.CharField("Nom", max_length=50)
    email = models.EmailField("Adresse email", max_length=250)
    phone = models.CharField("Numéro de téléphone", max_length=50, null=True, blank=True)

    role = models.ForeignKey(PeopleRole, verbose_name="Rôle", related_name="peoples", on_delete=models.SET_NULL,
                             null=True)
    mandate = models.ForeignKey(Mandate, verbose_name="Mandat", related_name="peoples", on_delete=models.CASCADE)

    class Meta(object):
        default_permissions = ('add', 'change', 'delete', 'admin',)

    def __str__(self):
        return self.first_name + " " + self.last_name.upper()


class DirectoryEntryManager(models.Manager):
    def get_last_for_association_id(self, association_id):
        return self.get_queryset()\
            .filter(association_id=association_id)\
            .order_by('-id')[:1][0]


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
    logo = models.ForeignKey('file.File', verbose_name="Logo", null=True, blank=True, on_delete=models.SET_NULL)

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
