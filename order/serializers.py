from rest_framework import serializers 
from order.models import Order,File
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from datetime import datetime, timedelta
from rest_framework.settings import api_settings
# from uploads.models import File
from model_DTO.validateError import validateError
from app.helper.order_helper.OrderUploadHelper import OrderUploadHelper


class OrderSerializer(serializers.Serializer):

    part_number = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    item_no = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    file_no = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    order_no = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    due_date = serializers.DateTimeField(format="%d/%m/%Y", input_formats=['%d/%m/%Y',],allow_null=True,required=False)
    order_qty = serializers.IntegerField(allow_null=True,required=False)
    package_no = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    package_name = serializers.CharField(max_length=500,allow_blank=True,allow_null=True,required=False)
    package_qty = serializers.DecimalField(allow_null=True,required=False,max_digits=5, decimal_places=2)
    route_code = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    route_trip = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    trip_no = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    history_updated = serializers.CharField(max_length=2000,allow_blank=True,allow_null=True,required=False)
    is_part_completed =  serializers.BooleanField(allow_null=True,required=False)
    is_route_completed =  serializers.BooleanField(allow_null=True,required=False)
    status = serializers.IntegerField(allow_null=True,required=False)
    is_deleted =  serializers.BooleanField(allow_null=True,required=False)
    is_updated =  serializers.BooleanField(allow_null=True,required=False)
    supplier_code = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    plant_code = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    project_code = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    pickup_no = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    created_by = serializers.CharField(max_length=15,allow_blank=True,allow_null=True,required=False)
    created_date = serializers.DateTimeField(allow_null=True,required=False)
    updated_by = serializers.CharField(max_length=15,allow_blank=True,allow_null=True,required=False)
    updated_date = serializers.DateTimeField(allow_null=True,required=False)


    order_count = serializers.IntegerField(allow_null=True,required=False)

    def create(self, validated_data):
       
        return Order.objects.create(**validated_data)



class Order_transaction_Serializer(serializers.Serializer):

    action = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    file_no = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    order_no = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    supplier_code = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    plant_code = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    part_number = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    part_name = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    due_date = serializers.DateTimeField(allow_null=True,required=False)
    order_qty = serializers.IntegerField(allow_null=True,required=False)
    package_no = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    package_qty =  serializers.IntegerField(allow_null=True,required=False)
    route_trip = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    updated_by = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    updated_date = serializers.DateTimeField(allow_null=True,required=False)

class Order_transaction_Serializer_DTO(serializers.Serializer):

    serviceStatus = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    massage = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    data = Order_transaction_Serializer()

class Order_transaction_list_Serializer_DTO(serializers.Serializer):

    serviceStatus = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    massage = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    data_list = Order_transaction_Serializer(many=True)
    csv_name = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)

class FileSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    file_no = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    file_name = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    file_size = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    order_count = serializers.IntegerField(allow_null=True,required=False)
    status = serializers.IntegerField(allow_null=True,required=False)
    customer_code = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    project_code = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    updated_by = serializers.CharField(allow_blank=True,allow_null=True,required=False)
    updated_date = serializers.DateTimeField(allow_null=True,required=False)
    file = serializers.FileField(required=False)


    def create(self, validated_data):

        validated_data['file_no'] = OrderUploadHelper.generate_file_no(validated_data['customer_code'])
        validated_data['status'] = 1
        validated_data['updated_date'] = datetime.utcnow()
    
        return File.objects.create(**validated_data)

class File_Serializer_DTO(serializers.Serializer):

    serviceStatus = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    massage = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    data = FileSerializer()

class File_list_Serializer_DTO(serializers.Serializer):

    serviceStatus = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    massage = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    data_list = FileSerializer(many=True)
    csv_name = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)


class validateErrorSerializer(serializers.Serializer):

    error = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    row = serializers.IntegerField(allow_null=True,required=False)
    column = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    status = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)


class validateErrorSerializerList(serializers.Serializer):

    serviceStatus = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    massage = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    validate_error_list = validateErrorSerializer(many=True)




class Search_miss_match_Serializer(serializers.Serializer):
    plant_code = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)

class Plant_list_Serializer_DTO(serializers.Serializer):

    serviceStatus = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    massage = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    data_list = Search_miss_match_Serializer(many=True)




class Order_list_Serializer_DTO(serializers.Serializer):

    serviceStatus = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    massage = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    csv_name = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    data_list = OrderSerializer(many=True)