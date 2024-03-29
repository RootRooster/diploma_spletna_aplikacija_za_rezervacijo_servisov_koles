# Generated by Django 5.0 on 2024-02-12 09:08

import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_rename_userinformation_profile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="address",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="phone_number",
            field=phonenumber_field.modelfields.PhoneNumberField(
                blank=True, max_length=128, null=True, region=None
            ),
        ),
    ]
