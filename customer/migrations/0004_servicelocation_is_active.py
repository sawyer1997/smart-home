# Generated by Django 4.2.7 on 2023-12-12 19:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("customer", "0003_alter_servicelocation_zipcode"),
    ]

    operations = [
        migrations.AddField(
            model_name="servicelocation",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]
