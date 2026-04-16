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
            "phone",
            "admin",
            "location",
            "available_beds",
            "available_icu_beds",
            "oxygen_level",
            "has_cardiology",
            "has_trauma",
            "is_available",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "admin", "created_at", "updated_at")


class HospitalResourceUpdateSerializer(serializers.ModelSerializer):
    """Used by hospital admins to update their resource/capacity status."""

    class Meta:
        model = Hospital
        fields = (
            "available_beds",
            "available_icu_beds",
            "oxygen_level",
            "has_cardiology",
            "has_trauma",
            "is_available",
        )
