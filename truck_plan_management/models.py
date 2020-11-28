from django.db import models
from datetime import datetime, timedelta
from decimal import Decimal
from django.utils import timezone


class PickUp(models.Model):

    pickup_no = models.CharField(max_length=150,blank=True, null=True)
    supplier_code  = models.CharField(max_length=50,blank=True, null=True)
    plant_code  = models.CharField(max_length=50,blank=True, null=True)
    due_date = models.DateTimeField(default=datetime.now(), blank=True)
    route_code = models.CharField(max_length=150,blank=True, null=True)
    route_trip = models.CharField(max_length=5,blank=True, null=True)
    status = models.IntegerField(blank=True,null=True)
    truckplan_no = models.CharField(max_length=150,blank=True, null=True,default="")
    is_active = models.BooleanField(default=True)
    updated_by = models.CharField(max_length=150,blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True,default=datetime.utcnow())

    def save(self, *args, **kwargs):

        if not self.pickup_no:

            self.updated_date = datetime.utcnow()

        return super(PickUp, self).save(*args, **kwargs)


class TruckPlan(models.Model):

    truckplan_no = models.CharField(max_length=150,blank=True, null=True)
    due_date = models.DateTimeField(default=datetime.now(), blank=True)
    route_code = models.CharField(max_length=150,blank=True, null=True)
    route_trip = models.CharField(max_length=5,blank=True, null=True)
    status = models.IntegerField(blank=True,null=True)
    is_active = models.BooleanField(default=True)
    updated_by = models.CharField(max_length=150,blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True,default=datetime.utcnow())

    def save(self, *args, **kwargs):

        if not self.truckplan_no:

            self.updated_date = datetime.utcnow()

        return super(TruckPlan, self).save(*args, **kwargs)