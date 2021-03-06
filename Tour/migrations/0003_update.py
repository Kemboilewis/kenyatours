# Generated by Django 3.1.3 on 2020-11-07 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tour', '0002_auto_20201107_1106'),
    ]

    operations = [
        migrations.CreateModel(
            name='update',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(max_length=100)),
                ('text', models.CharField(max_length=2000)),
                ('image', models.ImageField(upload_to='images/')),
                ('date_uploaded', models.DateField()),
            ],
        ),
    ]
