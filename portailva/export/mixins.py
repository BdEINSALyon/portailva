from django.contrib.auth.mixins import PermissionRequiredMixin


class AbleToExportMixin(PermissionRequiredMixin):
    permission_required = 'export.use'
    permission_denied_message = "Vous n'avez pas les permissions nécessaires pour exporter des données."
