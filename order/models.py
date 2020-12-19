from rest_framework import serializers
# from uploads.models import File
from model_DTO.validateError import validateError
from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone
from decimal import Decimal
from django.conf import settings
from app.helper.config.ConfigPart import ConfigPart
from app.helper.file_management.FileManagement import FileManagement



def upload_path_handler(instance, filename):
    
    configPart = ConfigPart()

    uploaded_part = FileManagement.validate_folder(configPart.configs.get("UPLOAD_ORDER_PART").data)
    
    return '{uploaded_part}{filename}'.format(uploaded_part=uploaded_part+"/", filename=filename)

class File(models.Model):

    file_no = models.CharField(max_length=150,blank=True, null=True,default='')
    file_name = models.CharField(max_length=150,blank=True, null=True)
    file_size = models.CharField(max_length=150,blank=True, null=True)
    order_count = models.IntegerField(blank=True,null=True)
    status = models.IntegerField(blank=True, null=True)
    customer_code = models.CharField(max_length=50,default='',blank=False, null=False)
    project_code = models.CharField(max_length=50,default='',blank=False, null=False)
    updated_by = models.CharField(max_length=150,blank=True, null=True)
    updated_date = models.DateTimeField(default=datetime.now(), blank=True)
    file = models.FileField(blank=False, null=False,upload_to=upload_path_handler)

    def save(self, *args, **kwargs):

        if not self.file_no:
            self.updated_date = datetime.utcnow()
        return super(File, self).save(*args, **kwargs)


class Order(models.Model):
    
    part_number = models.CharField(max_length=150,blank=False, default='')
    item_no = models.CharField(max_length=50,blank=False, default='')
    file_no = models.CharField(max_length=150,blank=False, default='')
    order_no = models.CharField(max_length=150,blank=False, default='')
    due_date = models.DateTimeField(default=datetime.now(), blank=True)
    order_qty = models.IntegerField(blank=True,null=True)
    package_no = models.CharField(max_length=150,blank=False, default='')
    package_qty = models.DecimalField(max_digits=20, decimal_places=2,blank=True, null=True)
    route_code = models.CharField(max_length=150,blank=False, default='')
    route_trip = models.CharField(max_length=150,blank=False, default='')
    history_updated = models.CharField(max_length=2000,blank=False, default='')
    is_part_completed = models.BooleanField(default=False)
    is_route_completed = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    supplier_code = models.CharField(max_length=150,blank=False, default='')
    plant_code = models.CharField(max_length=150,blank=False, default='')
    project_code = models.CharField(max_length=150,blank=False, default='')
    pickup_no = models.CharField(max_length=150,blank=False, default='')
    created_by = models.CharField(max_length=15,blank=True, null=True)
    created_date = models.DateTimeField(default=datetime.now(tz=timezone.utc),blank=True, null=True)
    updated_by = models.CharField(max_length=150,blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    



