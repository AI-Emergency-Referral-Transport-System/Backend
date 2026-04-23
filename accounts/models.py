from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from datetime import timedelta

from accounts.managers import UserManager
from common.models import TimestampedUUIDModel

class User(TimestampedUUIDModel, AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        PATIENT = "patient", "Patient"
        DRIVER = "driver", "Driver"
        HOSPITAL_ADMIN = "hospital_admin", "Hospital Admin"

    phone_number = models.CharField(max_length=32, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    role = models.CharField(max_length=32, choices=Role.choices, default=Role.PATIENT)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    # Useful for rate-limiting OTP delivery
    last_otp_sent = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []

    objects = UserManager()

    class Meta:
        ordering = ["-date_joined"]

    def __str__(self) -> str:
        return f"{self.email or self.phone_number or self.pk} ({self.role})"


class Profile(TimestampedUUIDModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    full_name = models.CharField(max_length=255, blank=True)
    emergency_contact = models.CharField(max_length=32, blank=True)
    blood_type = models.CharField(max_length=5, blank=True)
    location = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["user__phone_number"]

    def __str__(self) -> str:
        return f"Profile<{self.user.email or self.user.phone_number or self.user_id}>"


class OTPCode(TimestampedUUIDModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="otp_codes")
    code = models.CharField(max_length=255) # Hashed
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    @property
    def is_expired(self) -> bool:
        return timezone.now() >= self.expires_at

    def set_code(self, raw_code: str) -> None:
        """Hashes the OTP code before saving."""
        self.code = make_password(raw_code)

    def verify_code(self, raw_code: str) -> bool:
        """Checks raw OTP against hashed code."""
        return check_password(raw_code, self.code)
