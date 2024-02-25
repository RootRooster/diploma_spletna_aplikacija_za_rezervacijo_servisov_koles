# Generated by Django 5.0 on 2024-02-14 19:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0005_remove_fastserviceorder_completed_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="fastserviceorder",
            name="assigned_staff",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_assigned_staff",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="manualserviceorder",
            name="assigned_staff",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_assigned_staff",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
