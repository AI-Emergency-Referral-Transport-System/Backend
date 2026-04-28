import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create superuser from environment variables"

    def handle(self, *args, **options):
        User = get_user_model()

        username = os.environ.get("DJANGO_ADMIN_USERNAME")
        email = os.environ.get("DJANGO_ADMIN_EMAIL")
        password = os.environ.get("DJANGO_ADMIN_PASSWORD")

        if not all([email, password]):
            self.stdout.write(
                self.style.WARNING(
                    "Skipping: DJANGO_ADMIN_EMAIL or DJANGO_ADMIN_PASSWORD not set"
                )
            )
            return

        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.SUCCESS(f"Superuser '{email}' already exists, skipping")
            )
            return

        User.objects.create_superuser(
            email=email,
            password=password,
        )
        self.stdout.write(
            self.style.SUCCESS(f"Superuser '{email}' created successfully")
        )