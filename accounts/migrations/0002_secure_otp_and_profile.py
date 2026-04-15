import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="allergies",
        ),
        migrations.RemoveField(
            model_name="user",
            name="blood_type",
        ),
        migrations.RemoveField(
            model_name="user",
            name="emergency_contacts",
        ),
        migrations.RemoveField(
            model_name="user",
            name="first_name",
        ),
        migrations.RemoveField(
            model_name="user",
            name="last_name",
        ),
        migrations.RemoveField(
            model_name="user",
            name="medical_history",
        ),
        migrations.RemoveField(
            model_name="user",
            name="preferred_language",
        ),
        migrations.AddField(
            model_name="user",
            name="date_joined",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="user",
            name="is_verified",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="otpcode",
            name="code",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterModelOptions(
            name="user",
            options={"ordering": ["-date_joined"]},
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("full_name", models.CharField(blank=True, max_length=255)),
                ("emergency_contact", models.CharField(blank=True, max_length=32)),
                ("blood_type", models.CharField(blank=True, max_length=5)),
                ("location", models.CharField(blank=True, max_length=255)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["user__phone_number"],
            },
        ),
    ]
