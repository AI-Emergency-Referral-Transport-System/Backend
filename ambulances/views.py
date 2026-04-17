from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Ambulance
from .serializers import AmbulanceSerializer, AmbulanceStatusUpdateSerializer
from .services import AmbulanceDispatchService
from common.permissions import RolePermission


class AmbulanceListCreateAPIView(generics.ListCreateAPIView):
    queryset = Ambulance.objects.select_related("driver", "hospital")
    serializer_class = AmbulanceSerializer
    permission_classes = [RolePermission]
    allowed_roles = {"driver", "hospital_admin"}

    def get_queryset(self):
        #  Be able to filter available ambulances
        queryset = super().get_queryset()
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)
        return queryset

# 2. Driver Acceptance View 
class DriverAcceptEmergencyAPIView(APIView):
    """
    POST /api/driver/accept/{emergency_id}/

    """
    permission_classes = [IsAuthenticated, RolePermission]
    allowed_roles = {"driver"}

    def post(self, request, emergency_id):
        service = AmbulanceDispatchService()
        try:

            result = service.accept_emergency(
                driver_user=request.user, 
                emergency_id=emergency_id
            )
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

class AmbulanceStatusUpdateAPIView(generics.UpdateAPIView):
    """
    PUT /api/ambulances/{id}/status/
    Used by Flutter to move from 'en_route' to 'busy' or 'available'
    """
    queryset = Ambulance.objects.all()
    serializer_class = AmbulanceStatusUpdateSerializer
    permission_classes = [IsAuthenticated, RolePermission]
    allowed_roles = {"driver"}

    def perform_update(self, serializer):
        # Logical check: Only drivers can update their own status
        instance = self.get_object()
        if instance.driver != self.request.user:
            raise PermissionError("You cannot update an ambulance you are not driving.")
        serializer.save()