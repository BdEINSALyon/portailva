from django.conf.urls import url

from .views import DirectoryAPIView

urlpatterns = [
    url('^$', DirectoryAPIView.as_view(), name='api-v1-directory-index')
]
