# Generated by Django 5.1 on 2024-09-04 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0004_remove_reservation_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='state',
            field=models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')], default='pending', max_length=20),
        ),
    ]
