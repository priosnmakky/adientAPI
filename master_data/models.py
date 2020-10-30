from django.db import models
from datetime import datetime, timedelta
from decimal import Decimal
from django.utils import timezone


class Part(models.Model):

    part_number = models.CharField(max_length=150,blank=True, null=True)
    part_name = models.CharField(max_length=150,blank=True, null=True)
    service_type = models.CharField(max_length=50,blank=True, null=True)
    snp = models.IntegerField(blank=True, null=True,default=0)
    part_weight = models.DecimalField(max_digits=20, decimal_places=2,blank=True, null=True)
    remark = models.CharField(max_length=250,blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    project_code = models.CharField(max_length=150,blank=True, null=True)
    supplier_code  = models.CharField(max_length=50,blank=True, null=True)
    package_no = models.CharField(max_length=50,blank=True, null=True)
    package_volume = models.DecimalField(max_digits=20, decimal_places=2,blank=True, null=True)
    package_weight = models.DecimalField(max_digits=20, decimal_places=2,blank=True, null=True)
    is_active = models.BooleanField(default=True)
    updated_by = models.CharField(max_length=150,blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True,default=timezone.now)

    def save(self, *args, **kwargs):

        if not self.part_number:

            self.updated_date = datetime.utcnow()

        return super(Part, self).save(*args, **kwargs)


class RouterMaster(models.Model):

    route_no = models.CharField(max_length=250,blank=True, null=True)
    route_code = models.CharField(max_length=150,blank=True, null=True)
    route_trip = models.CharField(max_length=5,blank=True, null=True)
    supplier_code  = models.CharField(max_length=50,blank=True, null=True)
    plant_code = models.CharField(max_length=50,blank=True, null=True)
    pickup_before = models.IntegerField(blank=True, null=True)
    release_time = models.CharField(max_length=15,blank=True, null=True)
    pickup_time = models.CharField(max_length=15,blank=True, null=True)
    depart_time = models.CharField(max_length=15,blank=True, null=True)
    delivery_time = models.CharField(max_length=15,blank=True, null=True)
    complete_time = models.CharField(max_length=15,blank=True, null=True)
    transporter = models.CharField(max_length=50,blank=True, null=True)
    project_code = models.CharField(max_length=150,blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.CharField(max_length=15,blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now(),blank=True, null=True)
    updated_by = models.CharField(max_length=150,blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True,default=timezone.now)

    def save(self, *args, **kwargs):

        if not self.route_code:
            self.updated_date = datetime.utcnow()
        return super(RouterMaster, self).save(*args, **kwargs)

class RouterInfo(models.Model):

    project_code = models.CharField(max_length=150,blank=True, null=True)
    route_code = models.CharField(max_length=150,blank=True, null=True)
    trip_no = models.CharField(max_length=50,blank=True, null=True)
    truck_license = models.CharField(max_length=150,blank=True, null=True)
    province = models.CharField(max_length=150,blank=True, null=True)
    driver_code = models.CharField(max_length=150,blank=True, null=True)
    is_active = models.BooleanField(default=True)
    route_no = models.CharField(max_length=250,blank=True, null=True)
    updated_by = models.CharField(max_length=150,blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True,default=timezone.now)
   

    def save(self, *args, **kwargs):

        if not self.route_code:
            self.updated_date = datetime.utcnow()
        return super(RouterInfo, self).save(*args, **kwargs)


class CalendarMaster(models.Model):

    id = models.AutoField(primary_key=True)
    plant_code = models.CharField(max_length=150,blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)
    date = models.DateField( blank=True, null=True,default=timezone.now)
    remark = models.CharField(max_length=500,blank=True, null=True)
    is_working = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    updated_by = models.CharField(max_length=150,blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True,default=timezone.now)


    def save(self, *args, **kwargs):

        if not self.id:
            self.updated_date = datetime.utcnow()
        return super(CalendarMaster, self).save(*args, **kwargs)




# class Project(models.Model):

#     item_no = models.IntegerField(blank=False, null=False)
#     project_code = models.CharField(max_length=150,blank=True, null=True)
#     transporter = models.CharField(max_length=150,blank=True, null=True)
#     effective_date = models.DateTimeField(blank=True, null=True)
#     expire_date = models.DateTimeField(blank=True, null=True)
#     customer_code = models.CharField(max_length=150,blank=True, null=True)
#     # customer_description = models.CharField(max_length=150,blank=True, null=True)
#     created_by = models.CharField(max_length=15,blank=True, null=True)
#     created_date = models.DateTimeField(default=timezone.now(),blank=True, null=True)
#     updated_by = models.CharField(max_length=150,blank=True, null=True)
#     updated_date = models.DateTimeField(blank=True, null=True)

#     def save(self, *args, **kwargs):

#         if not self.id:
#             self.created_date = datetime.now()
#         return super(Project, self).save(*args, **kwargs)

class Project(models.Model):

    project_code = models.CharField(primary_key=True,max_length=150,blank=False, null=False,default="")
    remark = models.CharField(max_length=500,blank=True, null=True,default=None)
    updated_by = models.CharField(max_length=150,blank=False, null=False,default="")
    updated_date = models.DateTimeField(blank=False, null=False)
    customer_code = models.CharField(max_length=150,blank=False, null=False)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):

        # if not self.project_code:

        #     # self.updated_date = datetime.now()

        return super(Project, self).save(*args, **kwargs)

class Customer(models.Model):

    customer_code = models.CharField(primary_key=True,max_length=150,blank=False, null=False,default="")
    updated_by = models.CharField(max_length=150,blank=False, null=False,default="")
    updated_date = models.DateTimeField(blank=False, null=False,default=timezone.now)


    def save(self, *args, **kwargs):

        if not self.customer_code:
            self.updated_date = datetime.now()
        return super(Customer, self).save(*args, **kwargs)

class Station(models.Model):

    station_code =  models.CharField(primary_key=True,max_length=250,blank=False, null=False,default="")
    description = models.CharField(max_length=250,blank=True, null=True)
    station_type = models.CharField(max_length=250,blank=True, null=True)
    zone = models.CharField(max_length=250,blank=True, null=True)
    province = models.CharField(max_length=250,blank=True, null=True)
    address = models.CharField(max_length=350,blank=True, null=True)
    remark = models.CharField(max_length=500,blank=True, null=True)
    project_code = models.CharField(max_length=150,blank=False, null=False,default="")
    updated_by = models.CharField(max_length=150,blank=False, null=False,default="")
    updated_date = models.DateTimeField(blank=False, null=False,default=timezone.now)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):

        # if not self.station_code:
        #     self.created_date = datetime.now()
        return super(Station, self).save(*args, **kwargs)



class Package(models.Model):

    package_code = models.CharField(max_length=150,blank=True, null=True)
    package_no = models.CharField(max_length=150,blank=True, null=True)
    width = models.DecimalField(max_digits=20, decimal_places=2,blank=True, null=True)
    snp = models.IntegerField(blank=True, null=True)
    length = models.DecimalField(max_digits=20, decimal_places=2,blank=True, null=True)
    height = models.DecimalField(max_digits=20, decimal_places=2,blank=True, null=True)
    weight = models.DecimalField(max_digits=20, decimal_places=2,blank=True, null=True)
    station_code  = models.CharField(max_length=150,blank=True, null=True)
    image_url = models.CharField(max_length=250,blank=True, null=True)
    is_active = models.BooleanField(default=True)
    updated_by = models.CharField(max_length=150,blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True,default=timezone.now)

    def save(self, *args, **kwargs):

        if not self.package_no:
            self.updated_date = datetime.utcnow()
        return super(Package, self).save(*args, **kwargs)

class Truck(models.Model):

    truck_license = models.CharField(max_length=250,blank=False, null=False)
    province = models.CharField(max_length=250,blank=True, null=True)
    truck_type = models.CharField(max_length=250,blank=True, null=True)
    fuel_type = models.CharField(max_length=250,blank=True, null=True)
    max_speed = models.DecimalField(max_digits=20, decimal_places=2,blank=True, null=True)
    max_volume = models.DecimalField(max_digits=20, decimal_places=2,blank=True, null=True)
    max_weight = models.DecimalField(max_digits=20, decimal_places=2,blank=True, null=True)
    is_active = models.BooleanField(default=True)
    remark = models.CharField(max_length=500,blank=True, null=True)
    updated_by = models.CharField(max_length=150,blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True,default=timezone.now)

    def save(self, *args, **kwargs):

        if not self.truck_license:
            self.updated_date = datetime.utcnow()
        return super(Truck, self).save(*args, **kwargs)

class Driver(models.Model):

    driver_code = models.CharField(primary_key=True,max_length=250,blank=False, null=False)
    name = models.CharField(max_length=250,blank=True, null=True)
    tel = models.CharField(max_length=50,blank=True, null=True)
    is_active = models.BooleanField(default=True)
    remark = models.CharField(max_length=500,blank=True, null=True)
    updated_by = models.CharField(max_length=150,blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True,default=timezone.now)

    def save(self, *args, **kwargs):

        if not self.driver_code:
            self.updated_date = datetime.utcnow()
        return super(Driver, self).save(*args, **kwargs)


