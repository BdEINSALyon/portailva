from django.conf.urls import url

from portailva.association.views import AssociationDetailView, AssociationUpdateView, AssociationListView, \
    AssociationNewView, AssociationDeleteView, AssociationMandateListView, AssociationMandateNewView, \
    AssociationMandatePeopleNewView, AssociationMandatePeopleUpdateView, AssociationMandatePeopleDeleteView, \
    AssociationRequirementListView, AssociationRequirementAchieveView

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

    # Requirements
    url('^(?P<association_pk>\d+)/requirement/$', AssociationRequirementListView.as_view(),
        name='association-requirement-list'),
    url('^(?P<association_pk>\d+)/requirement/(?P<pk>\d+)/achieve/$', AssociationRequirementAchieveView.as_view(),
        name='association-requirement-achieve'),

    # Admin stuff
    url('^$', AssociationListView.as_view(), name='association-list'),
    url('^(?P<pk>\d+)/delete/$', AssociationDeleteView.as_view(), name='association-delete')

]