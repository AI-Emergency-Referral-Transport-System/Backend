from rest_framework import generics

from ai.models import AIMessage
from ai.serializers import AIMessageSerializer
from common.permissions import RolePermission


class AIMessageListCreateAPIView(generics.ListCreateAPIView):
    queryset = AIMessage.objects.select_related("emergency", "sender")
    serializer_class = AIMessageSerializer
    permission_classes = [RolePermission]
    allowed_roles = {"patient", "driver", "hospital_admin"}
