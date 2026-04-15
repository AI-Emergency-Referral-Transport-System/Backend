from django.urls import path

from ambulances.views import AmbulanceListCreateAPIView


urlpatterns = [
    path("", AmbulanceListCreateAPIView.as_view(), name="ambulance-list-create"),
]
