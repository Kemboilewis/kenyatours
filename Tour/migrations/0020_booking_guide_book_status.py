# Generated by Django 3.1.3 on 2020-12-04 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tour', '0019_auto_20201202_1057'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking_guide',
            name='book_status',
            field=models.BooleanField(default=False),
        ),
    ]
