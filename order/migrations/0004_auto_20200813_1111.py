# Generated by Django 2.2.8 on 2020-08-13 04:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20200812_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_datetime',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 8, 13, 11, 11, 6, 860459)),
        ),
    ]
