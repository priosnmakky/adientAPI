# Generated by Django 2.2.8 on 2020-10-27 07:06

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0040_auto_20201027_1225'),
    ]

    operations = [
        migrations.RenameField(
            model_name='file',
            old_name='customer_id',
            new_name='customer_code',
        ),
        migrations.RenameField(
            model_name='file',
            old_name='project_id',
            new_name='project_code',
        ),
        migrations.AlterField(
            model_name='file',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 10, 27, 14, 6, 30, 267459)),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 10, 27, 7, 6, 30, 268460, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='due_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 10, 27, 14, 6, 30, 268460)),
        ),
    ]