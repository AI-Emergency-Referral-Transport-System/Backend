import uuid
from django.db import models
from django.conf import settings


class AIMessage(models.Model):
    SENDER_CHOICES = [
        ('user', 'User'),
        ('ai', 'AI'),
        ('system', 'System'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    emergency = models.ForeignKey(
        'emergencies.EmergencyRequest',  # MUST EXIST
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='ai_messages'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ai_messages'
    )

    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    message = models.TextField()
    voice_url = models.URLField(blank=True, null=True)
    language = models.CharField(max_length=5, default='en')
    intent = models.CharField(max_length=50, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ai_messages'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender}: {self.message[:50]}"


class AIConversationSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ai_sessions'
    )

    session_id = models.CharField(max_length=100, unique=True)
    language = models.CharField(max_length=5, default='en')
    is_active = models.BooleanField(default=True)
    message_count = models.PositiveIntegerField(default=0)
    last_message_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ai_conversation_sessions'
        ordering = ['-created_at']  # FIXED

    def __str__(self):
        return f"Session {self.session_id} - {self.user}"