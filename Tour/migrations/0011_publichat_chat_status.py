# Generated by Django 3.1.3 on 2020-11-28 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tour', '0010_publichat'),
    ]

    operations = [
        migrations.AddField(
            model_name='publichat',
            name='chat_status',
            field=models.BooleanField(default=False),
        ),
    ]
