from django.conf.urls import url

from portailva.association.views import AssociationDetailView, AssociationUpdateView, AssociationListView, \
    AssociationNewView, AssociationDeleteView, AssociationMandateListView, AssociationMandateNewView, \
    AssociationMandatePeopleNewView, AssociationMandatePeopleUpdateView, AssociationMandatePeopleDeleteView, \
    AssociationRequirementListView, AssociationRequirementAchieveView, RequirementListView, RequirementDetailView, \
    BotInsaListView

urlpatterns = [
    # Association links
    url('^association/new/$', AssociationNewView.as_view(), name='association-new'),
    url('^association/(?P<pk>\d+)/$', AssociationDetailView.as_view(), name='association-detail'),
    url('^association/(?P<pk>\d+)/update/$', AssociationUpdateView.as_view(), name='association-update'),

    # Mandate
    url('^association/(?P<association_pk>\d+)/mandate/$', AssociationMandateListView.as_view(), name='association-mandate-list'),
    url('^association/(?P<association_pk>\d+)/mandate/new/$', AssociationMandateNewView.as_view(), name='association-mandate-new'),
    url('^association/(?P<association_pk>\d+)/mandate/(?P<mandate_pk>\d+)/people/new/$', AssociationMandatePeopleNewView.as_view(),
        name='association-mandate-people-new'),
    url('^association/(?P<association_pk>\d+)/mandate/(?P<mandate_pk>\d+)/people/(?P<pk>\d+)/edit/$',
        AssociationMandatePeopleUpdateView.as_view(), name='association-mandate-people-update'),
    url('^association/(?P<association_pk>\d+)/mandate/(?P<mandate_pk>\d+)/people/(?P<pk>\d+)/delete/$',
        AssociationMandatePeopleDeleteView.as_view(), name='association-mandate-people-delete'),

    # Requirements
    url('^association/(?P<association_pk>\d+)/requirement/$', AssociationRequirementListView.as_view(),
        name='association-requirement-list'),
    url('^association/(?P<association_pk>\d+)/requirement/(?P<pk>\d+)/achieve/$', AssociationRequirementAchieveView.as_view(),
        name='association-requirement-achieve'),

    # Admin stuff
    url('^association/$', AssociationListView.as_view(), name='association-list'),
    url('^requirement/$', RequirementListView.as_view(), name='requirement-list'),
    url('^requirement/(?P<pk>\d+)/$', RequirementDetailView.as_view(), name='requirement-detail'),
    url('^association/(?P<pk>\d+)/delete/$', AssociationDeleteView.as_view(), name='association-delete'),


    url('^association/botinsa0123/$', BotInsaListView.as_view(), name='botinsa')

]