from rest_framework import generics, permissions, response, status
from rest_framework.views import APIView

from accounts.models import User
from accounts.serializers import OTPRequestSerializer, UserSerializer
from accounts.services import OTPService
from common.permissions import RolePermission


class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [RolePermission]
    allowed_roles = {"hospital_admin"}


class OTPRequestAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = OTPRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = OTPService().queue_code(serializer.validated_data["phone_number"])
        return response.Response(payload, status=status.HTTP_202_ACCEPTED)
