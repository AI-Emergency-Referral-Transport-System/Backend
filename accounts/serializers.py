from rest_framework import serializers

from accounts.models import Profile, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "phone_number", "role", "is_verified")
        read_only_fields = fields


class OTPRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value: str) -> str:
        email = value.strip().lower()
        if not email:
            raise serializers.ValidationError("Email is required.")
        return email


class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6, min_length=6)

    def validate_email(self, value: str) -> str:
        email = value.strip().lower()
        if not email:
            raise serializers.ValidationError("Email is required.")
        return email

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
