# Generated by Django 3.1.3 on 2020-11-28 20:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Tour', '0011_publichat_chat_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='requested_by',
            new_name='requestUser',
        ),
    ]