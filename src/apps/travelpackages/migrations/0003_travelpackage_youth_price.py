# Generated by Django 5.1.4 on 2025-01-12 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travelpackages', '0002_travelpackage_is_always_available_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='travelpackage',
            name='youth_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
