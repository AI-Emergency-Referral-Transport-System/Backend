from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Matches /ws/tracking/<emergency_id>/
    re_path(
        r'ws/tracking/(?P<emergency_id>\w+)/$', 
        consumers.AmbulanceTrackingConsumer.as_asgi()
    ),

    # 2. For the Driver (Receiving new mission alerts)
    re_path(
        r'ws/dispatch/(?P<ambulance_id>\d+)/$', 
        consumers.DispatchConsumer.as_asgi()
    ),
]