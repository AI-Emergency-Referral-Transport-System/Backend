from rest_framework import generics

from common.permissions import RolePermission
from hospitals.models import Hospital
from hospitals.serializers import HospitalSerializer


class HospitalListCreateAPIView(generics.ListCreateAPIView):
    queryset = Hospital.objects.select_related("admin")
    serializer_class = HospitalSerializer
    permission_classes = [RolePermission]
    allowed_roles = {"driver", "hospital_admin"}
