# Generated by Django 3.1.3 on 2020-11-07 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tour', '0003_update'),
    ]

    operations = [
        migrations.CreateModel(
            name='hotel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotel_image', models.ImageField(upload_to='images/')),
                ('hotel_name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('town', models.CharField(max_length=100)),
                ('price', models.FloatField(max_length=100)),
                ('website', models.URLField(max_length=1000)),
                ('contacts', models.CharField(max_length=1000)),
            ],
        ),
    ]