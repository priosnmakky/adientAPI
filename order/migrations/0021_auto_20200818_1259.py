# Generated by Django 2.2.8 on 2020-08-18 05:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0020_auto_20200818_1252'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='plant',
            new_name='plant_code',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='supplier',
            new_name='supplier_code',
        ),
        migrations.AlterField(
            model_name='order',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 8, 18, 12, 59, 45, 971537), null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='due_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 8, 18, 12, 59, 45, 971537)),
        ),
    ]
