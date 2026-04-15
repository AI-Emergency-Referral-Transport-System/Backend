from rest_framework import generics

from common.permissions import RolePermission
from emergencies.models import Emergency
from emergencies.serializers import EmergencySerializer


class EmergencyListCreateAPIView(generics.ListCreateAPIView):
    queryset = Emergency.objects.select_related("patient", "ambulance", "hospital")
    serializer_class = EmergencySerializer
    permission_classes = [RolePermission]
    allowed_roles = {"patient", "driver", "hospital_admin"}
