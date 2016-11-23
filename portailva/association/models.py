import json
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

from portailva.file.models import AssociationFile


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
        ordering = ('position',)

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
        ordering = ('role',)

    def __str__(self):
        return self.first_name + " " + self.last_name.upper()


class RequirementManager(models.Manager):
    def get_all_active(self):
        return self.all().filter(active_until__lt=datetime.now())


class Requirement(models.Model):
    """
    A Requirement represents an action that an Association can accomplish.
    """
    REQUIREMENT_TYPES = (
        ('mandate', 'Mandat'),
        ('file', 'Fichier'),
        ('accomplishment', 'Validation manuelle')
    )
    name = models.CharField("Nom", max_length=100)
    type = models.CharField("Type de condition", max_length=40, choices=REQUIREMENT_TYPES)
    data = models.TextField("Meta données", blank=True, default='{}')
    help_text = models.TextField("Texte d'aide", blank=True, null=True)

    active_until = models.DateTimeField("Date de fin de validité")

    objects = RequirementManager()

    def __str__(self):
        return '[' + self.type + '] ' + self.name

    def is_achieved(self, association_id):
        data = json.loads(self.data)
        achieved = False
        if self.type == 'file':
            tag_id = int(self.data['tag_id'])
            nb_files = AssociationFile.objects \
                .filter(association__id=association_id) \
                .filter(tags__id__exact=tag_id) \
                .count()
            if nb_files > 0:
                achieved = True

        if self.type == 'mandate':
            year = data['year']
            try:
                last_mandate = Mandate.objects \
                                   .filter(association__id=association_id) \
                                   .filter(ends_at__year=int(year)) \
                                   .order_by('-ends_at')[0:1].get()
                if last_mandate is not None:
                    people = People.objects.filter(mandate__id=last_mandate.id).count()
                    if people > 2:
                        achieved = True
            except Mandate.DoesNotExist:
                pass

        if self.type == 'accomplishment':
            accomplishment = Accomplishment.objects \
                .filter(requirement__id=self.id) \
                .filter(association__id=association_id) \
                .count()
            if accomplishment > 0:
                achieved = True
        return achieved


class Accomplishment(models.Model):
    """
    An Accomplishment is used to achieve a Requirement manually.
    """
    association = models.ForeignKey(Association, verbose_name="Association", on_delete=models.CASCADE)
    requirement = models.ForeignKey(Requirement, verbose_name="Condition", limit_choices_to={'type': 'accomplishment'},
                                    on_delete=models.CASCADE)

    created_at = models.DateTimeField("Date d'ajout", auto_now_add=True)
    updated_at = models.DateTimeField("Dernière mise à jour", auto_now=True)

    class Meta(object):
        default_permissions = ('achieve', 'unachieve',)

    def __str__(self):
        return '[' + self.association.name + '] ' + self.requirement.name
