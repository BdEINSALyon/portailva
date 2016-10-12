from django.conf.urls import url

from portailva.association.views import AssociationDetailView

urlpatterns = [
    url('^(?P<pk>\d+)/$', AssociationDetailView.as_view(), name='association-detail')
]