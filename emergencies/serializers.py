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
            "emergency_type",
            "priority",
            "status",
            "requested_location",
            "patient_description",
            "notes",
            "completed_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "patient", "status", "completed_at", "created_at", "updated_at")


class EmergencyDetailSerializer(serializers.ModelSerializer):
    """Full read serializer with nested names for detail view."""
    requested_location = GeometryField(required=False, allow_null=True)
    patient_name = serializers.CharField(source="patient.name", read_only=True)
    hospital_name = serializers.CharField(source="hospital.name", read_only=True, default=None)

    class Meta:
        model = Emergency
        fields = (
            "id",
            "patient",
            "patient_name",
            "ambulance",
            "hospital",
            "hospital_name",
            "emergency_type",
            "priority",
            "status",
            "requested_location",
            "patient_description",
            "notes",
            "completed_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


class EmergencySelectHospitalSerializer(serializers.Serializer):
    """Accepts a hospital ID so the patient can confirm their chosen hospital."""
    hospital_id = serializers.UUIDField()


class EmergencyNotesUpdateSerializer(serializers.ModelSerializer):
    """Allows drivers and hospital admins to add/update notes on an emergency."""

    class Meta:
        model = Emergency
        fields = ("notes",)
