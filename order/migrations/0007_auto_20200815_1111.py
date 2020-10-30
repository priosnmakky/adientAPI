# Generated by Django 2.2.8 on 2020-08-15 04:11

import datetime
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_auto_20200813_1210'),
    ]

    operations = [
        migrations.CreateModel(
            name='part_master',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.IntegerField()),
                ('part_number', models.CharField(default='', max_length=150)),
                ('part_name', models.CharField(default='', max_length=150)),
                ('service_type', models.CharField(default='', max_length=50)),
                ('snp', models.IntegerField(blank=True, null=True)),
                ('part_weight', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=20)),
                ('remark', models.CharField(default='', max_length=250)),
                ('updated_by', models.CharField(default='', max_length=50)),
                ('uploaded_datetime', models.DateTimeField(blank=True, default=datetime.datetime(2020, 8, 15, 11, 11, 30, 305437))),
                ('project_code', models.CharField(default='', max_length=150)),
                ('supplier_code', models.CharField(default='', max_length=50)),
                ('package_no', models.CharField(default='', max_length=50)),
            ],
        ),
        migrations.RenameField(
            model_name='order',
            old_name='supplier_name',
            new_name='file_id',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='order_amount',
            new_name='order_qty',
        ),
        migrations.RemoveField(
            model_name='order',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='order',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='order',
            name='file_no',
        ),
        migrations.RemoveField(
            model_name='order',
            name='order_datetime',
        ),
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
        migrations.RemoveField(
            model_name='order',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='order',
            name='updated_date',
        ),
        migrations.AddField(
            model_name='order',
            name='due_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 8, 15, 11, 11, 30, 301749)),
        ),
        migrations.AddField(
            model_name='order',
            name='order_no',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.AddField(
            model_name='order',
            name='package_no',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.AddField(
            model_name='order',
            name='package_qty',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='route_trip',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='supplier',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.AddField(
            model_name='order',
            name='uploaded_by',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.AddField(
            model_name='order',
            name='uploaded_datetime',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 8, 15, 11, 11, 30, 301749)),
        ),
    ]
