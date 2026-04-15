from django.urls import path

from hospitals.views import HospitalListCreateAPIView


urlpatterns = [
    path("", HospitalListCreateAPIView.as_view(), name="hospital-list-create"),
]
