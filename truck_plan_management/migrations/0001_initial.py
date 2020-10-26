# Generated by Django 2.2.8 on 2020-09-29 06:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PickUp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pickup_no', models.CharField(blank=True, max_length=150, null=True)),
                ('supplier_code', models.CharField(blank=True, max_length=50, null=True)),
                ('plant_code', models.CharField(blank=True, max_length=50, null=True)),
                ('order_count', models.IntegerField(blank=True, null=True)),
                ('due_date', models.DateField(blank=True, null=True, verbose_name='Date')),
                ('route_code', models.CharField(blank=True, max_length=150, null=True)),
                ('trip_no', models.CharField(blank=True, max_length=5, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('updated_by', models.CharField(blank=True, max_length=150, null=True)),
                ('updated_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
            ],
        ),
    ]
