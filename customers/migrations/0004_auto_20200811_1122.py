# Generated by Django 2.2.8 on 2020-08-11 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_auto_20200811_1041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='lat',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='long',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='remark',
            field=models.CharField(blank=True, default='', max_length=250, null=True),
        ),
    ]
