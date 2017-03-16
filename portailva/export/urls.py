from django.conf.urls import url

from portailva.export.views import ExportView

urlpatterns = [
    url('^$', ExportView.as_view(), name='export')
]
