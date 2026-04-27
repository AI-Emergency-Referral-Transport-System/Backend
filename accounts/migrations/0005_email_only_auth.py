from django.db import migrations, models


def blank_phone_numbers_to_null(apps, schema_editor):
    User = apps.get_model("accounts", "User")
    User.objects.filter(phone_number="").update(phone_number=None)


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_driverprofile_hospitalprofile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="phone_number",
            field=models.CharField(blank=True, max_length=32, null=True, unique=True),
        ),
        migrations.RunPython(blank_phone_numbers_to_null, migrations.RunPython.noop),
    ]
