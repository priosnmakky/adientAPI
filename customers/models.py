from django.db import models
from datetime import datetime, timedelta

class Customer(models.Model):
    item = models.IntegerField(blank=False, null=False)
    name = models.CharField(max_length=150,blank=False, default='')
    project = models.CharField(max_length=150,blank=False, default='')
    statio_code = models.CharField(max_length=150,blank=False, default='')
    description = models.CharField(max_length=350,blank=False, default='')
    customers_type = models.CharField(max_length=150,blank=False, default='')
    zone = models.CharField(max_length=150,blank=False, default='')
    province = models.CharField(max_length=150,blank=False, default='')
    address = models.CharField(max_length=350,blank=False, default='')
    lat = models.CharField(max_length=200,null=True, blank=True, default='')
    long = models.CharField(max_length=200,null=True, blank=True, default='')
    remark = models.CharField(max_length=250,null=True, blank=True, default='')
    # customer_code = models.CharField(max_length=150,blank=False, default='')
    # customer_description = models.CharField(max_length=250,blank=False, default='')
    # project_code = models.CharField(max_length=250,blank=False, default='')
    # transporter = models.CharField(max_length=250,blank=False, default='')
    # effective_date = models.DateTimeField(default=datetime.now(), blank=True)
    # expire_date = models.DateTimeField(default=datetime.now(), blank=True)

# Create your models here.
