# Generated by Django 2.2.8 on 2020-08-12 04:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_auto_20200812_0009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='effective_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 8, 12, 11, 27, 57, 610710)),
        ),
        migrations.AlterField(
            model_name='project',
            name='expire_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 8, 12, 11, 27, 57, 610710)),
        ),
    ]