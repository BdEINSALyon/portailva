from django.conf.urls import url

urlpatterns = [
    url('^association/(?P<association_pk>\d+)/article/$', AssociationarticleListView.as_view(),
        name='association-article-list'),
    url('^association/(?P<association_pk>\d+)/article/new/$', AssociationarticleNewView.as_view(),
        name='association-article-new'),
    url('^association/(?P<association_pk>\d+)/article/(?P<pk>\d+)/$', AssociationarticleDetailView.as_view(),
        name='association-article-detail'),
    url('^association/(?P<association_pk>\d+)/article/(?P<pk>\d+)/update/$', AssociationarticleUpdateView.as_view(),
        name='association-article-update'),
    url('^association/(?P<association_pk>\d+)/article/(?P<pk>\d+)/delete/$', AssociationarticleDeleteView.as_view(),
        name='association-article-delete'),
]
