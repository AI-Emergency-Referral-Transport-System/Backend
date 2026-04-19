from rest_framework import serializers

from ai.models import AIMessage


class AIMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIMessage
        fields = (
            "id",
            "emergency",
            "sender",
            "role",
            "content",
            "created_at",
        )
        read_only_fields = ("id", "created_at")
