# Generated by Django 2.2.8 on 2020-10-27 04:47

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0037_auto_20201027_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 27, 11, 47, 24, 634924)),
        ),
        migrations.AlterField(
            model_name='file',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 10, 27, 11, 47, 24, 634924)),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 10, 27, 4, 47, 24, 635921, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='due_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 10, 27, 11, 47, 24, 635921)),
        ),
    ]