from django.db import models


# Create your models here.
class Place(models.Model):
    """
    A Place somewhere.
    """
    name = models.CharField("Nom", max_length=50)
    loc_x = models.DecimalField("Latitude", max_digits=8, decimal_places=6)
    loc_y = models.DecimalField("Longitude", max_digits=8, decimal_places=6)

    class Meta(object):
        default_permissions = ('add', 'change', 'delete', 'admin',)

    def __str__(self):
        return self.name + " (" + str(self.loc_x) + ", " + str(self.loc_y) + ")"
