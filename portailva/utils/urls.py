from django.conf.urls import url

from portailva.utils.views import PlaceListView, PlaceNewView, PlaceUpdateView, PlaceDeleteView

urlpatterns = [
    # Admin stuff
    url('^place/$', PlaceListView.as_view(), name='place-list'),
    url('^place/new/$', PlaceNewView.as_view(), name='place-new'),
    url('^place/(?P<pk>\d+)/edit/', PlaceUpdateView.as_view(), name='place-update'),
    url('^place/(?P<pk>\d+)/delete/', PlaceDeleteView.as_view(), name='place-delete')
]
