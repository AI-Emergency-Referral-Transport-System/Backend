from django.urls import path

from emergencies.views import EmergencyListCreateAPIView


urlpatterns = [
    path("", EmergencyListCreateAPIView.as_view(), name="emergency-list-create"),
]
