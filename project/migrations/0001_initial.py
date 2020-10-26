# Generated by Django 2.2.8 on 2020-08-11 13:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.IntegerField()),
                ('customer_code', models.CharField(default='', max_length=150)),
                ('customer_description', models.CharField(default='', max_length=250)),
                ('project_code', models.CharField(default='', max_length=250)),
                ('transporter', models.CharField(default='', max_length=250)),
                ('effective_date', models.DateTimeField(blank=True, default=datetime.datetime(2020, 8, 11, 20, 53, 42, 312701))),
                ('expire_date', models.DateTimeField(blank=True, default=datetime.datetime(2020, 8, 11, 20, 53, 42, 312701))),
            ],
        ),
    ]
