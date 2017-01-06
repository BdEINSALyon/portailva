from django.conf.urls import url

from portailva.newsletter.views import AssociationArticleListView, AssociationArticleNewView, \
    AssociationArticleDetailView, AssociationArticleUpdateView, AssociationArticleDeleteView

urlpatterns = [
    url('^association/(?P<association_pk>\d+)/article/$', AssociationArticleListView.as_view(),
        name='association-article-list'),
    url('^association/(?P<association_pk>\d+)/article/new/$', AssociationArticleNewView.as_view(),
        name='association-article-new'),
    url('^association/(?P<association_pk>\d+)/article/(?P<pk>\d+)/$', AssociationArticleDetailView.as_view(),
        name='association-article-detail'),
    url('^association/(?P<association_pk>\d+)/article/(?P<pk>\d+)/update/$', AssociationArticleUpdateView.as_view(),
        name='association-article-update'),
    url('^association/(?P<association_pk>\d+)/article/(?P<pk>\d+)/delete/$', AssociationArticleDeleteView.as_view(),
        name='association-article-delete'),
]
