from django.conf.urls import url

from portailva.association.views import AssociationDetailView, AssociationUpdateView

urlpatterns = [
    # Association links
    url('^(?P<pk>\d+)/$', AssociationDetailView.as_view(), name='association-detail'),
    url('^(?P<pk>\d+)/update/$', AssociationUpdateView.as_view(), name='association-update')
]