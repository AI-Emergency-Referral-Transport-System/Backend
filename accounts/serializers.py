from rest_framework import serializers

from accounts.models import Profile, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "phone_number", "email", "role", "is_verified")
        read_only_fields = fields


class OTPRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=32)

    def validate_phone_number(self, value: str) -> str:
        phone_number = value.strip()
        if not phone_number:
            raise serializers.ValidationError("Phone number is required.")
        return phone_number


class OTPVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=32)
    code = serializers.CharField(max_length=6, min_length=6)

    def validate_phone_number(self, value: str) -> str:
        phone_number = value.strip()
        if not phone_number:
            raise serializers.ValidationError("Phone number is required.")
        return phone_number

    def validate_code(self, value: str) -> str:
        code = value.strip()
        if not code.isdigit():
            raise serializers.ValidationError("Verification code must contain digits only.")
        return code


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "full_name",
            "emergency_contact",
            "blood_type",
            "location",
            "updated_at",
        )
        read_only_fields = ("id", "user", "updated_at")
