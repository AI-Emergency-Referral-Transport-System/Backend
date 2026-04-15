from rest_framework import generics

from ambulances.models import Ambulance
from ambulances.serializers import AmbulanceSerializer
from common.permissions import RolePermission


class AmbulanceListCreateAPIView(generics.ListCreateAPIView):
    queryset = Ambulance.objects.select_related("driver", "hospital")
    serializer_class = AmbulanceSerializer
    permission_classes = [RolePermission]
    allowed_roles = {"driver", "hospital_admin"}
