# Generated by Django 2.2.8 on 2020-08-10 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.IntegerField()),
                ('name', models.CharField(default='', max_length=150)),
                ('project', models.CharField(default='', max_length=150)),
                ('statio_code', models.CharField(default='', max_length=150)),
                ('description', models.CharField(default='', max_length=350)),
                ('customers_type', models.CharField(default='', max_length=150)),
                ('zone', models.CharField(default='', max_length=150)),
                ('province', models.CharField(default='', max_length=150)),
                ('address', models.CharField(default='', max_length=350)),
                ('lat', models.CharField(default='', max_length=200)),
                ('long', models.CharField(default='', max_length=200)),
                ('remark', models.CharField(default='', max_length=250)),
            ],
        ),
    ]
