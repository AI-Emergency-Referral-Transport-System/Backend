from rest_framework import generics

from common.permissions import RolePermission
from tracking.models import LocationUpdate
from tracking.serializers import LocationUpdateSerializer


class LocationUpdateListCreateAPIView(generics.ListCreateAPIView):
    queryset = LocationUpdate.objects.select_related("ambulance", "reported_by")
    serializer_class = LocationUpdateSerializer
    permission_classes = [RolePermission]
    allowed_roles = {"driver", "hospital_admin"}
