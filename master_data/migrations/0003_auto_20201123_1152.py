# Generated by Django 2.2.8 on 2020-11-23 04:52

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('master_data', '0002_auto_20201121_1427'),
    ]

    operations = [
        migrations.RenameField(
            model_name='routerinfo',
            old_name='trip_no',
            new_name='route_trip',
        ),
        migrations.AlterField(
            model_name='routermaster',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 23, 4, 52, 27, 908339, tzinfo=utc), null=True),
        ),
    ]