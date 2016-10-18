from django.conf.urls import url

from portailva.file.views import FileListView

urlpatterns = [
    # Admin stuff
    url('^$', FileListView.as_view(), name='file-list'),
]