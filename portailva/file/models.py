import uuid

from django.conf import settings
from django.db import models
from django.dispatch import receiver

from portailva.association.models import Association


class FileType(models.Model):
    """
    A FileType defines characteristics of a file (extension, MIME type, etc.).
    """
    name = models.CharField("Nom", max_length=50)
    mime_type = models.CharField("Type MIME", max_length=100)

    def __str__(self):
        return self.name


class File(models.Model):
    """
    A File.
    """
    name = models.CharField("Nom", max_length=200)

    created_at = models.DateTimeField("Date d'ajout", auto_now_add=True)
    updated_at = models.DateTimeField("Dernière mise à jour", auto_now=True)

    class Meta(object):
        default_permissions = ('add', 'change', 'delete', 'admin',)

    def __str__(self):
        return self.name

    def can_access(self, user):
        # By default, user must be logged in
        if user is not None and user.is_authenticated():
            # If file is an association file, we ensure user belongs to association or is an admin
            if isinstance(self, AssociationFile):
                return self.association.can_access(user)
            else:
                return True
        return False


class FileFolder(models.Model):
    """
    A File Folder is used for Association File sorting.
    """
    name = models.CharField("Nom", max_length=250)
    description = models.TextField("Description")
    position = models.IntegerField("Position", blank=True)
    is_writable = models.BooleanField("Accessible en écriture ?", default=True)

    parent = models.ForeignKey('self', verbose_name="Dossier parent", null=True, blank=True, on_delete=models.SET_NULL)
    allowed_types = models.ManyToManyField(FileType, verbose_name="Extensions autorisées", blank=True)

    def __str__(self):
        return self.name

    def get_all_children(self, include_self=True):
        r = []
        if include_self:
            r.append(self)
        for c in FileFolder.objects.filter(parent=self):
            r.append(c.get_all_children(include_self=False))

    def get_tree(self):
        tree = []
        if self.parent is not None:
            tree.extend(self.parent.get_tree())
        tree.append(self.name)
        return tree

    def get_path(self):
        tree = self.get_tree()
        return '/'.join(tree)


class AssociationFile(File):
    association = models.ForeignKey(Association, related_name="files", verbose_name="Association", null=True,
                                    blank=True, on_delete=models.CASCADE)
    folder = models.ForeignKey(FileFolder, verbose_name="Dossier", related_name="files", on_delete=models.CASCADE)


def user_directory_path(instance, filename):
    return 'uploads/' + str(uuid.uuid1())


class FileVersion(models.Model):
    """
    A specific File Version.
    """
    version = models.IntegerField("Numéro de version")
    data = models.FileField(upload_to=user_directory_path, verbose_name="Version")

    file = models.ForeignKey(File, verbose_name="Fichier", related_name="versions", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Utilisateur", null=True, on_delete=models.SET_NULL)

    created_at = models.DateTimeField("Date d'ajout", auto_now_add=True)
    updated_at = models.DateTimeField("Dernière mise à jour", auto_now=True)

    def __str__(self):
        return 'Version ' + str(self.version)


@receiver(models.signals.pre_delete, sender=FileVersion)
def file_version_delete(sender, instance, **kwargs):
    instance.data.delete(False)
