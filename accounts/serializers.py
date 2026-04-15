from rest_framework import serializers

from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "phone_number",
            "first_name",
            "last_name",
            "email",
            "role",
            "created_at",
        )
        read_only_fields = ("id", "created_at")


class OTPRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=32)
