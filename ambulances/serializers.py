from rest_framework import serializers

from ambulances.models import Ambulance


class AmbulanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ambulance
        fields = (
            "id",
            "code",
            "driver",
            "hospital",
            "status",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")
