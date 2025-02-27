# Generated by Django 5.1.4 on 2025-01-12 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_booking_email_booking_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='order_id',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='booking',
            name='payment_id',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='booking',
            name='payment_response',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='payment_status',
            field=models.CharField(default='pending', max_length=20),
        ),
    ]
