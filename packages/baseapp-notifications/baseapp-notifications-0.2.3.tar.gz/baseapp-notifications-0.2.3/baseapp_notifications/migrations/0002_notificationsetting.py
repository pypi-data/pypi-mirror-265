# Generated by Django 4.2.10 on 2024-02-08 13:53

import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("baseapp_notifications", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="NotificationSetting",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="modified"
                    ),
                ),
                (
                    "channel",
                    models.IntegerField(
                        choices=[(0, "All"), (1, "Email"), (2, "Push"), (3, "In-App")]
                    ),
                ),
                ("verb", models.CharField(max_length=255)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notifications_settings",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "swappable": "BASEAPP_NOTIFICATIONS_NOTIFICATIONSETTING_MODEL",
            },
        ),
    ]
