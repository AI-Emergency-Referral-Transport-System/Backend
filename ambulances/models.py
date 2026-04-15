from django.conf import settings
from django.db import models

from common.models import TimestampedUUIDModel


class Ambulance(TimestampedUUIDModel):
    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        DISPATCHED = "dispatched", "Dispatched"
        OFFLINE = "offline", "Offline"

    code = models.CharField(max_length=64, unique=True)
    driver = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_ambulance",
        limit_choices_to={"role": "driver"},
    )
    hospital = models.ForeignKey(
        "hospitals.Hospital",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ambulances",
    )
    status = models.CharField(max_length=32, choices=Status.choices, default=Status.AVAILABLE)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["code"]

    def __str__(self) -> str:
        return self.code
