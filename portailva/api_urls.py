from django.conf.urls import url, include

urlpatterns = [
    # API v1
    url(r'^v1/directory/', include('portailva.directory.api_v1.urls')),
]
