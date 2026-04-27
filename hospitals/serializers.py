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
            "facility_type",
            "address",
            "city",
            "region",
            "phone",
            "email",
            "admin",
            "location",
            "total_beds",
            "available_beds",
            "occupied_beds",
            "total_icu_beds",
            "available_icu_beds",
            "occupied_icu_beds",
            "oxygen_level",
            "services",
            "departments",
            "specialties",
            "has_emergency",
            "has_icu",
            "has_surgery",
            "has_cardiology",
            "has_trauma",
            "has_maternity",
            "has_neonatal",
            "is_available",
            "verification_status",
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
            "occupied_beds",
            "available_icu_beds",
            "occupied_icu_beds",
            "oxygen_level",
            "services",
            "has_cardiology",
            "has_trauma",
            "is_available",
        )
