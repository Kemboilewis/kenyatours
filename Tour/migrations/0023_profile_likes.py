# Generated by Django 3.1.3 on 2020-12-07 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tour', '0022_booking_guide_guide_response'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='likes',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
    ]
