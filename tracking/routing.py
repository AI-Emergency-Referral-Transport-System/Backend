from django.urls import re_path

from tracking.consumers import TrackingConsumer


websocket_urlpatterns = [
    re_path(r"^ws/tracking/(?P<ambulance_id>[0-9a-f-]+)/$", TrackingConsumer.as_asgi()),
]
