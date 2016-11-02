from django.conf.urls import url

from portailva.association.views import AssociationDetailView, AssociationUpdateView, AssociationListView, \
    AssociationNewView, AssociationDeleteView, AssociationMandateListView, AssociationMandateNewView, \
    AssociationMandatePeopleNewView, AssociationMandatePeopleUpdateView, AssociationMandatePeopleDeleteView

urlpatterns = [
    # Association links
    url('^new/$', AssociationNewView.as_view(), name='association-new'),
    url('^(?P<pk>\d+)/$', AssociationDetailView.as_view(), name='association-detail'),
    url('^(?P<pk>\d+)/update/$', AssociationUpdateView.as_view(), name='association-update'),

    # Mandate
    url('^(?P<association_pk>\d+)/mandate/$', AssociationMandateListView.as_view(), name='association-mandate-list'),
    url('^(?P<association_pk>\d+)/mandate/new/$', AssociationMandateNewView.as_view(), name='association-mandate-new'),
    url('^(?P<association_pk>\d+)/mandate/(?P<mandate_pk>\d+)/people/new/$', AssociationMandatePeopleNewView.as_view(),
        name='association-mandate-people-new'),
    url('^(?P<association_pk>\d+)/mandate/(?P<mandate_pk>\d+)/people/(?P<pk>\d+)/edit/$',
        AssociationMandatePeopleUpdateView.as_view(), name='association-mandate-people-update'),
    url('^(?P<association_pk>\d+)/mandate/(?P<mandate_pk>\d+)/people/(?P<pk>\d+)/delete/$',
        AssociationMandatePeopleDeleteView.as_view(), name='association-mandate-people-delete'),

    # Admin stuff
    url('^$', AssociationListView.as_view(), name='association-list'),
    url('^(?P<pk>\d+)/delete/$', AssociationDeleteView.as_view(), name='association-delete')

]