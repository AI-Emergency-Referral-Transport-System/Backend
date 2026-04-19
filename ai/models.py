from django.conf import settings
from django.db import models

from common.models import TimestampedUUIDModel


class RAGKnowledge(TimestampedUUIDModel):
    title = models.CharField(max_length=255)
    content = models.TextField()
    source_url = models.URLField(blank=True)
    embedding_key = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title


class AIMessage(TimestampedUUIDModel):
    class Role(models.TextChoices):
        SYSTEM = "system", "System"
        USER = "user", "User"
        ASSISTANT = "assistant", "Assistant"

    emergency = models.ForeignKey(
        "emergencies.Emergency",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ai_messages",
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ai_messages",
    )
    role = models.CharField(max_length=32, choices=Role.choices, default=Role.USER)
    content = models.TextField()

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return f"{self.role} message"
