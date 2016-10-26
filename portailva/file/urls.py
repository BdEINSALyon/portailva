from django.conf.urls import url

from portailva.file.views import FileListView, FileView

urlpatterns = [
    url('^(?P<pk>\d+)/$', FileView.as_view(), name='file-view'),

    # Admin stuff
    url('^$', FileListView.as_view(), name='file-list'),
]
