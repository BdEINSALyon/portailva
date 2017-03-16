from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin, AccessMixin


class AbleToExportMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return self.handle_no_permission()
        return super(AbleToExportMixin, self).dispatch(request, *args, **kwargs)