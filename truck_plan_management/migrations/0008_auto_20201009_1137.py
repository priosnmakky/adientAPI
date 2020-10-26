# Generated by Django 2.2.8 on 2020-10-09 04:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('truck_plan_management', '0007_auto_20201006_1714'),
    ]

    operations = [
        migrations.CreateModel(
            name='TruckPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('truckPlan_no', models.CharField(blank=True, max_length=150, null=True)),
                ('due_date', models.DateField(blank=True, null=True, verbose_name='Date')),
                ('route_code', models.CharField(blank=True, max_length=150, null=True)),
                ('route_trip', models.CharField(blank=True, max_length=5, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('updated_by', models.CharField(blank=True, max_length=150, null=True)),
                ('updated_date', models.DateTimeField(blank=True, default=datetime.datetime(2020, 10, 9, 4, 37, 14, 463913), null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='pickup',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 10, 9, 4, 37, 14, 462912), null=True),
        ),
    ]
