from rest_framework import serializers
from uploads.models import File
from model_DTO.validateError import validateError
from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone
from decimal import Decimal


class FileSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    file_no = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    file_name = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    file_size = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    order_count = serializers.IntegerField(allow_null=True,required=False)
    status = serializers.IntegerField(allow_null=True,required=False)
    customer_id = serializers.IntegerField(allow_null=True,required=False)
    project_id = serializers.IntegerField(allow_null=True,required=False)
    created_by = serializers.CharField(max_length=15,allow_blank=True,allow_null=True,required=False)
    created_date = serializers.DateTimeField(format="%d-%m-%Y ", input_formats=['%d-%m-%Y',],default=datetime.now(tz=timezone.utc),allow_null=True,required=False)
    updated_by = serializers.CharField(allow_blank=True,allow_null=True,required=False)
    updated_date = serializers.DateTimeField(format="%d-%m-%Y", input_formats=['%d-%m-%Y',],default=datetime.now(tz=timezone.utc),allow_null=True,required=False)
    file = serializers.FileField()


    class Meta:     #instead of meta write Meta (Capital M)
        model = File
        fields = '__all__'
 

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return File.objects.create(**validated_data)


class Order(models.Model):
    part_number = models.CharField(max_length=150,blank=False, default='')
    item_no = models.CharField(max_length=50,blank=False, default='')
    file_id = models.CharField(max_length=150,blank=False, default='')
    order_id = models.CharField(max_length=150,blank=False, default='')
    due_date = models.DateTimeField(default=datetime.now(), blank=True)
    order_qty = models.IntegerField(blank=True,null=True)
    package_no = models.CharField(max_length=150,blank=False, default='')
    package_qty = models.DecimalField(max_digits=20, decimal_places=2,blank=True, null=True)
    route_code = models.CharField(max_length=150,blank=False, default='')
    route_trip = models.CharField(max_length=150,blank=False, default='')
    trip_no = models.CharField(max_length=150,blank=False, default='')
    history_updated = models.CharField(max_length=2000,blank=False, default='')
    is_part_completed = models.BooleanField(default=False)
    is_route_completed = models.BooleanField(default=False)
    status = models.IntegerField(blank=True,null=True)
    is_deleted = models.BooleanField(default=False)
    is_updated = models.BooleanField(default=False)
    supplier_no = models.CharField(max_length=150,blank=False, default='')
    plant_no = models.CharField(max_length=150,blank=False, default='')
    project_code = models.CharField(max_length=150,blank=False, default='')
    pickup_no = models.CharField(max_length=150,blank=False, default='')
    created_by = models.CharField(max_length=15,blank=True, null=True)
    created_date = models.DateTimeField(default=datetime.now(tz=timezone.utc),blank=True, null=True)
    updated_by = models.CharField(max_length=150,blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    


    # def save(self, *args, **kwargs):
    #     # This means that the model isn't saved to the database yet
    #     # if self._state.adding:
    #     #     # Get the maximum display_id value from the database
    #     order_no = self.objects.id
    #     if order_no is not None:
    #             self.order_id = order_id + 1

    #         # # aggregate can return None! Check it first.
    #         # # If it isn't none, just use the last ID specified (which should be the greatest) and add one to it
    #         # if last_id is not None:
    #         #     self.display_id = last_id + 1

    #     super(Order, self).save(*args, **kwargs)

# class part_master(models.Model):
#     item = models.IntegerField(blank=False, null=False)
#     part_number = models.CharField(max_length=150,blank=False, default='')
#     part_name = models.CharField(max_length=150,blank=False, default='')
#     service_type = models.CharField(max_length=50,blank=False, default='')
#     snp = models.IntegerField(blank=True,null=True)
#     part_weight = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal(0.00))
#     remark = models.CharField(max_length=250,blank=False, default='')
#     updated_by = models.CharField(max_length=50,blank=False, default='')
#     uploaded_datetime = models.DateTimeField(default=datetime.now(), blank=True)
#     project_code = models.CharField(max_length=150,blank=False, default='')
#     supplier_code  = models.CharField(max_length=50,blank=False, default='')
#     package_no = models.CharField(max_length=50,blank=False, default='')


# class router_master(models.Model):

#     item = models.IntegerField(blank=False, null=False)
#     route_code = models.CharField(max_length=150,blank=False, default='')
#     trip_no = models.CharField(max_length=5,blank=False, default='')
#     supplier_code  = models.CharField(max_length=50,blank=False, default='')
#     plant_code = models.CharField(max_length=50,blank=False, default='')
#     release_datetime = models.DateTimeField(default=datetime.now(), blank=True)
#     pickup_datetime = models.DateTimeField( blank=True)
#     depart_datetime = models.DateTimeField( blank=True)
#     delivery_datetime = models.DateTimeField( blank=True)
#     complete_datetime = models.DateTimeField( blank=True)
#     transporter = models.CharField(max_length=50,blank=False, default='')






