# Generated by Django 2.2.8 on 2020-08-18 17:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0028_auto_20200818_2205'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='project_code',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.AddField(
            model_name='order',
            name='route_code',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.AddField(
            model_name='order',
            name='trip_no',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 8, 19, 0, 50, 48, 469018), null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='due_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 8, 19, 0, 50, 48, 469018)),
        ),
    ]