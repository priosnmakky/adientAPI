from django.db import models
from datetime import datetime, timedelta

class Part_master(models.Model):
    item_on= models.IntegerField(blank=False, null=False)
    part_number = models.CharField(max_length=150,blank=False, default='')
    part_name = models.CharField(max_length=150,blank=False, default='')
    supplier_code = models.CharField(max_length=150,blank=False, default='')
    project_code  = models.CharField(max_length=150,blank=False, default='')

