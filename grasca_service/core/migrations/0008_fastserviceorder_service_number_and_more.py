# Generated by Django 5.0 on 2024-02-16 08:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "core",
            "0007_remove_fastserviceorder_core_fastserviceorder_date_not_sunday_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="fastserviceorder",
            name="service_number",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="manualserviceorder",
            name="service_number",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
