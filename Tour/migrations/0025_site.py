# Generated by Django 3.1.3 on 2020-12-12 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tour', '0024_auto_20201209_0853'),
    ]

    operations = [
        migrations.CreateModel(
            name='site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('site_image', models.ImageField(upload_to='images/')),
                ('location', models.CharField(max_length=500)),
                ('description', models.CharField(max_length=2000)),
            ],
        ),
    ]
