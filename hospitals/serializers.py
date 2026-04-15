from rest_framework import serializers
from rest_framework_gis.fields import GeometryField

from hospitals.models import Hospital


class HospitalSerializer(serializers.ModelSerializer):
    location = GeometryField()

    class Meta:
        model = Hospital
        fields = (
            "id",
            "name",
            "admin",
            "location",
            "capacity_total",
            "capacity_available",
            "is_available",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")
