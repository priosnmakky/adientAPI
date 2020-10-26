# Generated by Django 2.2.8 on 2020-08-15 15:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_auto_20200815_1145'),
    ]

    operations = [
        migrations.DeleteModel(
            name='part_master',
        ),
        migrations.DeleteModel(
            name='router_master',
        ),
        migrations.AlterField(
            model_name='order',
            name='due_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 8, 15, 22, 42, 58, 784018)),
        ),
        migrations.AlterField(
            model_name='order',
            name='uploaded_datetime',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 8, 15, 22, 42, 58, 784018)),
        ),
    ]
