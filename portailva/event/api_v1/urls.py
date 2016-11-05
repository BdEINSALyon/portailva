from django.conf.urls import url

from portailva.event.api_v1.views import EventListAPIView

urlpatterns = [
    url(r'^$', EventListAPIView.as_view(), name='api-v1-event-index')
]
