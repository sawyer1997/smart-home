# Generated by Django 4.2.7 on 2023-11-30 18:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("customer", "0002_alter_servicelocation_zipcode"),
    ]

    operations = [
        migrations.AlterField(
            model_name="servicelocation",
            name="zipcode",
            field=models.CharField(
                default="00000",
                help_text="Enter the zipcode",
                validators=[django.core.validators.MinLengthValidator(5)],
                verbose_name="ZipCode",
            ),
        ),
    ]