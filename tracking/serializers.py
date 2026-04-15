from rest_framework import serializers
from rest_framework_gis.fields import GeometryField

from tracking.models import LocationUpdate


class LocationUpdateSerializer(serializers.ModelSerializer):
    location = GeometryField()

    class Meta:
        model = LocationUpdate
        fields = (
            "id",
            "ambulance",
            "reported_by",
            "location",
            "heading",
            "speed",
            "recorded_at",
            "created_at",
        )
        read_only_fields = ("id", "created_at")
