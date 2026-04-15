from rest_framework import serializers
from rest_framework_gis.fields import GeometryField

from emergencies.models import Emergency


class EmergencySerializer(serializers.ModelSerializer):
    requested_location = GeometryField(required=False, allow_null=True)

    class Meta:
        model = Emergency
        fields = (
            "id",
            "patient",
            "ambulance",
            "hospital",
            "status",
            "requested_location",
            "summary",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")
