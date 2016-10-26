from django.db import models
from django.contrib.auth.models import User


# Create your models here.
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
            if user.is_superuser or user.has_perm('association.can_admin_association'):
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
            if user.is_superuser:
                return True
            elif user in self.users.all():
                return True

        return False

