# Generated by Django 3.1.3 on 2020-11-07 08:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Tour', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='sencondname',
            new_name='secondname',
        ),
    ]