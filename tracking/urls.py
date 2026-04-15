from django.urls import path

from tracking.views import LocationUpdateListCreateAPIView


urlpatterns = [
    path("locations/", LocationUpdateListCreateAPIView.as_view(), name="location-update-list-create"),
]
