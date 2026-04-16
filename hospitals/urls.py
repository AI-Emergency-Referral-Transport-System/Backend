from django.urls import path

from hospitals.views import (
    HospitalListCreateAPIView,
    HospitalDetailAPIView,
    HospitalResourceUpdateAPIView,
    HospitalIncomingEmergenciesAPIView,
    HospitalApproveEmergencyAPIView,
    HospitalRejectEmergencyAPIView,
    HospitalPatientArrivedAPIView,
    HospitalNearbyAPIView,
)

urlpatterns = [
    # Public / shared
    path("", HospitalListCreateAPIView.as_view(), name="hospital-list-create"),
    path("nearby/", HospitalNearbyAPIView.as_view(), name="hospital-nearby"),
    path("<uuid:pk>/", HospitalDetailAPIView.as_view(), name="hospital-detail"),

    # Hospital admin operations
    path("resources/", HospitalResourceUpdateAPIView.as_view(), name="hospital-resources"),
    path("incoming/", HospitalIncomingEmergenciesAPIView.as_view(), name="hospital-incoming"),
    path("approve/<uuid:emergency_id>/", HospitalApproveEmergencyAPIView.as_view(), name="hospital-approve"),
    path("reject/<uuid:emergency_id>/", HospitalRejectEmergencyAPIView.as_view(), name="hospital-reject"),
    path("arrived/<uuid:emergency_id>/", HospitalPatientArrivedAPIView.as_view(), name="hospital-arrived"),
]
