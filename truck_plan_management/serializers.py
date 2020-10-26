from rest_framework import serializers 
from truck_plan_management.models import PickUp,TruckPlan
from order.models import Order
from datetime import datetime
from app.helper.generate_PUS.Generate_PUS import Genetate_PUS
from app.helper.generate_PUS.GenerateTruckPlan import GenerateTruckPlan
from app.helper.config.ConfigMessage import ConfigMessage
configMessage = ConfigMessage()


class PickUp_Serializer(serializers.Serializer):

    pickup_no = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    supplier_code  = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    plant_code  = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    due_date = serializers.DateField(format="%d/%m/%Y", input_formats=['%d/%m/%Y',],allow_null=True,required=False)
    route_code = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    route_trip = serializers.CharField(max_length=5,allow_blank=True,allow_null=True,required=False)
    truckplan_no = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    is_active = serializers.BooleanField(required=False)
    updated_by = serializers.CharField(allow_blank=True,allow_null=True,required=False)
    updated_date = serializers.DateTimeField(allow_null=True,required=False)
    order_count = serializers.IntegerField(allow_null=True,required=False,read_only=True)
    status = serializers.IntegerField(allow_null=True,required=False)

    pickup_before = serializers.IntegerField( allow_null=True,required=False)
    release_time = serializers.CharField(max_length=15,allow_blank=True, allow_null=True,required=False)
    pickup_time = serializers.CharField(max_length=15,allow_blank=True, allow_null=True,required=False)
    depart_time = serializers.CharField(max_length=15,allow_blank=True, allow_null=True,required=False)
    delivery_time = serializers.CharField(max_length=15,allow_blank=True, allow_null=True,required=False)
    complete_time = serializers.CharField(max_length=15,allow_blank=True, allow_null=True,required=False)
    
    truck_license = serializers.CharField(max_length=250,allow_blank=True,allow_null=True,required=False)
    name = serializers.CharField(max_length=250,allow_blank=True,allow_null=True,required=False)

    def update(self, instance, validated_data):

        instance.pickup_no = validated_data.get('pickup_no', instance.pickup_no)
        instance.supplier_code = validated_data.get('supplier_code', instance.supplier_code)
        instance.plant_code = validated_data.get('plant_code', instance.plant_code)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.route_code = validated_data.get('route_code', instance.route_code)
        instance.route_trip = validated_data.get('route_trip', instance.route_trip)
        instance.is_active = True
        instance.updated_by = validated_data.get('updated_by', instance.updated_by)
        instance.updated_date = datetime.utcnow()
        instance.save()

    def validate_due_date(self, due_date):
        print(due_date)
        if due_date is None :

            raise serializers.ValidationError(detail=configMessage.configs.get("UPLOAD_PICKUP_DUEDATE_REQUIRED").data)
        return datetime.strptime(str(due_date), "%Y-%m-%d").date() 

    def create(self, validated_data):

        order_obj = Order.objects.filter(
            supplier_no=validated_data.get('supplier_code'),
            plant_no=validated_data.get('plant_code'),
            route_code=validated_data.get('route_code'),
            route_trip=validated_data.get('route_trip'),
            due_date__year=validated_data.get('due_date').year,
            due_date__month=validated_data.get('due_date').month,
            due_date__day=validated_data.get('due_date').day,
            is_deleted=False,
            is_route_completed=True,
            is_part_completed=True
            )

        due_date_str = str(validated_data.get('due_date').year) + "{0:0=2d}".format(int(validated_data.get('due_date').month)) + "{0:0=2d}".format(int(validated_data.get('due_date').day)) 
        genetate_PUS_obj = Genetate_PUS(validated_data.get('supplier_code'),due_date_str) 
        pickup_no = genetate_PUS_obj.generate_PUS() 

        validated_data['pickup_no'] = pickup_no
        validated_data['status'] = 2
        
 
        order_obj.update(pickup_no=validated_data.get('pickup_no'),updated_date=datetime.utcnow(),updated_by=validated_data.get('updated_by'))
        print(validated_data)
        return PickUp.objects.create(**validated_data)

class PickUp_Serializer_DTO(serializers.Serializer):

    serviceStatus = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    massage = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    data = PickUp_Serializer()

class PickUp_list_Serializer_DTO(serializers.Serializer):

    serviceStatus = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    massage = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    data_list = PickUp_Serializer(many=True)
    csv_name = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)


class TruckPlan_Serializer(serializers.Serializer):


    truckplan_no = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    due_date = serializers.DateField(format="%d/%m/%Y", input_formats=['%d/%m/%Y',],allow_null=True,required=False)
    route_code = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    route_trip = serializers.CharField(max_length=5,allow_blank=True,allow_null=True,required=False)
    is_active = serializers.BooleanField(required=False)
    updated_by = serializers.CharField(allow_blank=True,allow_null=True,required=False)
    updated_date = serializers.DateTimeField(allow_null=True,required=False)
    pickUp_count = serializers.IntegerField(allow_null=True,required=False,read_only=True)
    status = serializers.IntegerField(allow_null=True,required=False)

    release_time = serializers.CharField(max_length=15,allow_blank=True, allow_null=True,required=False,read_only=True)
    delivery_time = serializers.CharField(max_length=15,allow_blank=True, allow_null=True,required=False,read_only=True)
    truck_license = serializers.CharField(max_length=250,allow_blank=True,allow_null=True,required=False,read_only=True)
    name = serializers.CharField(max_length=250,allow_blank=True,allow_null=True,required=False,read_only=True
    
    
    )

    def update(self, instance, validated_data):

        instance.truckplan_no = validated_data.get('truckplan_no', instance.truckplan_no)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.route_code = validated_data.get('route_code', instance.route_code)
        instance.route_trip = validated_data.get('route_trip', instance.route_trip)
        instance.is_active = True
        instance.updated_by = validated_data.get('updated_by', instance.updated_by)
        instance.updated_date = datetime.utcnow()
        instance.save()

    def create(self, validated_data):

        pickUp_obj = PickUp.objects.filter(
            route_code=validated_data.get('route_code'),
            route_trip=validated_data.get('route_trip'),
            due_date__year=validated_data.get('due_date').year,
            due_date__month=validated_data.get('due_date').month,
            due_date__day=validated_data.get('due_date').day,
            is_active=True,
            status=2
            )

        due_date_str = str(validated_data.get('due_date').year) + "{0:0=2d}".format(int(validated_data.get('due_date').month)) + "{0:0=2d}".format(int(validated_data.get('due_date').day)) 
        generate_truck_plan_obj = GenerateTruckPlan(validated_data.get('route_code'),validated_data.get('route_trip'),due_date_str) 
        truckPlan_no = generate_truck_plan_obj.generate_truck_plan() 

        validated_data['truckplan_no'] = truckPlan_no
        validated_data['status'] = 2

        print(validated_data)
 
        pickUp_obj.update(truckplan_no=validated_data.get('truckplan_no'),updated_date=datetime.utcnow(),updated_by=validated_data.get('updated_by'))
        return TruckPlan.objects.create(**validated_data)

class TruckPlan_Serializer_DTO(serializers.Serializer):

    serviceStatus = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    massage = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    data = TruckPlan_Serializer()

class TruckPlan_list_Serializer_DTO(serializers.Serializer):

    serviceStatus = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    massage = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    data_list = TruckPlan_Serializer(many=True)
    csv_name = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)

