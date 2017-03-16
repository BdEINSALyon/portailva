from django.views.generic import TemplateView

from portailva.export.forms import ExportForm
from portailva.export.mixins import AbleToExportMixin


class ExportView(AbleToExportMixin, TemplateView):
    template_name = 'export/export.html'

    def get_context_data(self, **kwargs):
        return {
            'form': ExportForm()
        }
