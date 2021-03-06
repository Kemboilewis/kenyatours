# Generated by Django 3.1.3 on 2021-02-22 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Tour', '0032_auto_20210222_1228'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activity',
            options={'verbose_name': 'Activitity', 'verbose_name_plural': 'Activitiies'},
        ),
        migrations.AlterModelOptions(
            name='booking_guide',
            options={'verbose_name': 'Booking Tour Guide', 'verbose_name_plural': 'Bookings for Tour Guide'},
        ),
        migrations.AlterModelOptions(
            name='event',
            options={'verbose_name': 'Event', 'verbose_name_plural': 'Events'},
        ),
        migrations.AlterModelOptions(
            name='hotel',
            options={'verbose_name': 'Hotel', 'verbose_name_plural': 'Hotels'},
        ),
        migrations.AlterModelOptions(
            name='message',
            options={'verbose_name': 'Message', 'verbose_name_plural': 'Messages'},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'User_Profile', 'verbose_name_plural': 'User Profiles'},
        ),
        migrations.AlterModelOptions(
            name='publichat',
            options={'verbose_name': 'public-chat', 'verbose_name_plural': 'Public Chats'},
        ),
        migrations.AlterModelOptions(
            name='site',
            options={'verbose_name': 'Attraction site', 'verbose_name_plural': 'Attraction Sites'},
        ),
        migrations.AlterModelOptions(
            name='update',
            options={'verbose_name': 'New', 'verbose_name_plural': 'News'},
        ),
    ]
