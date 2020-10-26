from rest_framework import serializers
from uploads.models import File
from master_data.models import Part,RouterMaster,Project,Customer,Package,Station,Truck,Driver,RouterInfo,CalendarMaster
from datetime import datetime, timedelta
from datetime import timezone
from master_data import views 
import re
from app.helper.config.ConfigMessage import ConfigMessage
configMessage = ConfigMessage()

class Part_Serializer(serializers.Serializer):

    part_number = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    part_name = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    service_type = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    snp = serializers.IntegerField(allow_null=True,required=False)
    remark = serializers.CharField(max_length=250,allow_blank=True,allow_null=True,required=False)
    project_code = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    supplier_code  = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    package_no = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    status = serializers.IntegerField(allow_null=True,required=False)
    created_by = serializers.CharField(max_length=15,allow_blank=True,allow_null=True,required=False)
    created_date = serializers.DateTimeField(allow_null=True,required=False)
    updated_by = serializers.CharField(allow_blank=True,allow_null=True,required=False)
    updated_date = serializers.DateTimeField(allow_null=True,required=False)
    package_volume = serializers.DecimalField(allow_null=True,required=False,max_digits=20, decimal_places=2)
    package_weight = serializers.DecimalField(allow_null=True,required=False,max_digits=20, decimal_places=2)

    def update(self, instance, validated_data):

        # instance.part_name = validated_data.get('part_name', instance.part_name)
        print("update")
        instance.service_type = validated_data.get('service_type', instance.service_type)
        instance.remark = validated_data.get('remark', instance.remark)
        instance.project_code = validated_data.get('project_code', instance.project_code)
        instance.supplier_code = validated_data.get('supplier_code', instance.supplier_code)
        instance.status = validated_data.get('status', instance.status)
        instance.package_no = validated_data.get('package_no', instance.package_no)
        instance.package_volume = validated_data.get('package_volume', instance.package_volume)
        instance.package_weight = validated_data.get('package_weight', instance.package_weight)
        instance.updated_date = datetime.utcnow()
        instance.save()

        return instance
    

    def create(self, validated_data):
        # print(validated_data)
       
        return Part.objects.create(**validated_data)

class Part_Serializer_DTO(serializers.Serializer):

    serviceStatus = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    massage = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    data = Part_Serializer()

class Part_list_Serializer_DTO(serializers.Serializer):

    serviceStatus = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    csv_name = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    massage = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    data_list = Part_Serializer(many=True)

class RouterInfo_Serializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    project_code = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    route_code = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    trip_no = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    truck_license = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    province = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    driver_code = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    driver_name = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    route_no = serializers.CharField(max_length=250,allow_blank=True,allow_null=True,required=False)
    updated_by = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    updated_date = serializers.DateTimeField(allow_null=True,required=False)


    def update(self, instance, validated_data):

        # instance.part_name = validated_data.get('part_name', instance.part_name)
        instance.project_code = validated_data.get('project_code', instance.project_code)
        instance.route_code = validated_data.get('route_code', instance.route_code)
        instance.trip_no = validated_data.get('trip_no', instance.trip_no)
        instance.truck_license = validated_data.get('truck_license', instance.truck_license)
        instance.province = validated_data.get('province', instance.province)
        instance.driver_code = validated_data.get('driver_code', instance.driver_code)
        instance.route_no = validated_data.get('route_no', instance.route_no)
        instance.updated_by = validated_data.get('updated_by', instance.updated_by)
        instance.updated_date = datetime.utcnow()
        instance.save()

        return instance
    

    def create(self, validated_data):
        # print(validated_data)
       
        return RouterInfo.objects.create(**validated_data)

class RouterInfo_Serializer_DTO(serializers.Serializer):

    serviceStatus = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    massage = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    data = RouterInfo_Serializer()

class RouterInfo_list_Serializer_DTO(serializers.Serializer):

    serviceStatus = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    csv_name = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    massage = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    data_list = RouterInfo_Serializer(many=True)


class CalendarMaster_Serializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    plant_code = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    day = serializers.IntegerField(allow_null=True,required=False)
    date = serializers.DateField(allow_null=True,required=False,format="%Y-%m-%d")
    remark = serializers.CharField(max_length=500,allow_blank=True,allow_null=True,required=False)
    is_working = serializers.BooleanField(required=False)
    is_active = serializers.BooleanField(required=False)
    updated_by = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    updated_date = serializers.DateTimeField(allow_null=True,required=False)


    def update(self, instance, validated_data):

        instance.remark = validated_data.get('remark', instance.remark)
        instance.is_working = validated_data.get('is_working', instance.is_working)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.updated_by = validated_data.get('updated_by', instance.updated_by)
        instance.updated_date = datetime.utcnow()
        instance.save()

        return instance
    

    def create(self, validated_data):

        return CalendarMaster.objects.create(**validated_data)

class CalendarMaster_Serializer_DTO(serializers.Serializer):

    serviceStatus = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    massage = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    data = CalendarMaster_Serializer()

class CalendarMaster_list_Serializer_DTO(serializers.Serializer):

    serviceStatus = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    csv_name = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    massage = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    data_list = CalendarMaster_Serializer(many=True)

    
class validate_error_serializer(serializers.Serializer):

    error = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    row = serializers.IntegerField(allow_null=True,required=False)
    column = serializers.IntegerField(allow_null=True,required=False)
    status = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)

class validate_warning_serializer(serializers.Serializer):

    error = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    row = serializers.IntegerField(allow_null=True,required=False)
    status = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)

class RouterMaster_Serializer(serializers.Serializer):


    customer_code = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    project_code = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    route_no = serializers.CharField(max_length=250,allow_blank=True,allow_null=True,required=False)
    route_code = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    trip_no = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    supplier_code = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    plant_code = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    pickup_before = serializers.IntegerField(allow_null=True,required=False)
    release_time = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    pickup_time = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    depart_time = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    delivery_time = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    complete_time = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    updated_by = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    updated_date = serializers.DateTimeField(allow_null=True,required=False)

    time_rex = re.compile("([0-2]|""){1}[0-9]{1}[.][0-5]{1}[0-9]{1}")

    def validate_project_code(self, project_code):
        
        print(project_code)
        if project_code is None or project_code.strip() == "" :

            raise serializers.ValidationError(detail=configMessage.configs.get("ROUTE_MASTER_PROJECTCODE_REQUIRED").data)
        
        return project_code

    def validate_route_code(self, route_code):

        if route_code is None or route_code.strip() == "" :

            raise serializers.ValidationError(detail=configMessage.configs.get("ROUTE_MASTER_ROUTECODE_REQUIRED").data)
        return route_code
    
    def validate_trip_no(self, trip_no):

        if trip_no is None or trip_no.strip() == "" :

            raise serializers.ValidationError(detail=configMessage.configs.get("ROUTE_MASTER_TRIPNO_REQUIRED").data)
        
        return trip_no
    
    def validate_supplier_code(self, supplier_code):

        if supplier_code is None or supplier_code.strip() == "" :

            raise serializers.ValidationError(detail=configMessage.configs.get("ROUTE_MASTER_SUPPLIERCODE_REQUIRED").data)
        
        return supplier_code
    
    def validate_plant_code(self, plant_code):

        if plant_code is None or plant_code.strip() == "" :

            raise serializers.ValidationError(detail=configMessage.configs.get("ROUTE_MASTER_PLANTCODE_REQUIRED").data)
        
        return plant_code
    
    def validate_pickup_before(self, pickup_before):

        if pickup_before is None or pickup_before == "" :

            raise serializers.ValidationError(detail=configMessage.configs.get("ROUTE_MASTER_PICKUPBEFORE_REQUIRED").data)
        
        return pickup_before
    
    
    def validate_release_time(self, release_time):

        if release_time is None or release_time.strip() == "" :

            raise serializers.ValidationError(detail=configMessage.configs.get("ROUTE_MASTER_RELEASETIME_REQUIRED").data)
        
        elif not self.time_rex.match(release_time ) :

            raise serializers.ValidationError(detail=configMessage.configs.get("ROUTE_MASTER_RELEASETIME_INCORRECT_FORMAT").data)

        return release_time
    
    def validate_pickup_time(self, pickup_time):

        if pickup_time is None or pickup_time.strip() == "" :

            raise serializers.ValidationError(detail=configMessage.configs.get("ROUTE_MASTER_PICKUPTIME_REQUIRED").data)
        
        elif not self.time_rex.match(pickup_time ) :

            raise serializers.ValidationError(detail=configMessage.configs.get("ROUTE_MASTER_PICKUPTIME_INCORRECT_FORMAT").data)

        return pickup_time
    
    def validate_depart_time(self, depart_time):

        if depart_time is None or depart_time.strip() == "" :

            raise serializers.ValidationError(detail=configMessage.configs.get("ROUTE_MASTER_DEPARTTIME_REQUIRED").data)
        
        elif not self.time_rex.match(depart_time ) :

            raise serializers.ValidationError(detail=configMessage.configs.get("ROUTE_MASTER_DEPARTTIME_INCORRECT_FORMAT").data)

        return depart_time
    
    def validate_delivery_time(self, delivery_time):

        if delivery_time is None or delivery_time.strip() == "" :

            raise serializers.ValidationError(detail=configMessage.configs.get("ROUTE_MASTER_DELIVERYTIME_REQUIRED").data)
        
        elif not self.time_rex.match(delivery_time ) :

            raise serializers.ValidationError(detail=configMessage.configs.get("ROUTE_MASTER_DELIVERYTIME_INCORRECT_FORMAT").data)

        return delivery_time
    
    def validate_complete_time(self, complete_time):

        if complete_time is None or complete_time.strip() == "" :

            raise serializers.ValidationError(detail=configMessage.configs.get("ROUTE_MASTER_COMPLETETIME_REQUIRED").data)
        
        elif not self.time_rex.match(complete_time ) :

            raise serializers.ValidationError(detail=configMessage.configs.get("ROUTE_MASTER_COMPLETETIME_INCORRECT_FORMAT").data)

        return complete_time
    
    

    def update(self, instance, validated_data):

        instance.project_code = validated_data.get('project_code', instance.project_code)
        instance.route_no = validated_data.get('route_no', instance.route_no)
        instance.route_code = validated_data.get('route_code', instance.route_code)
        instance.trip_no = validated_data.get('trip_no', instance.trip_no)
        instance.supplier_code = validated_data.get('supplier_code', instance.supplier_code)
        instance.plant_code = validated_data.get('plant_code', instance.plant_code)
        instance.pickup_before = validated_data.get('pickup_before', instance.pickup_before)
        instance.release_time = validated_data.get('release_time', instance.release_time)
        instance.pickup_time = validated_data.get('pickup_time', instance.pickup_time)
        instance.depart_time = validated_data.get('depart_time', instance.depart_time)
        instance.delivery_time = validated_data.get('delivery_time', instance.delivery_time)
        instance.complete_time = validated_data.get('complete_time', instance.complete_time)
        instance.updated_by = validated_data.get('updated_by', instance.updated_by)
        instance.updated_date = datetime.utcnow()
        instance.save()

        return instance
    

    def create(self, validated_data):
    
        validated_data['route_no'] = validated_data['route_code']+ "-" + validated_data['trip_no'] + "-" + validated_data['supplier_code'] + "-" + validated_data['plant_code']
        return RouterMaster.objects.create(**validated_data)

  

class RouterMaster_Serializer_DTO(serializers.Serializer):

    serviceStatus = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    massage = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    data = RouterMaster_Serializer()

class RouterMaster_list_Serializer_DTO(serializers.Serializer):

    serviceStatus = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    massage = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    data_list = RouterMaster_Serializer(many=True)
    csv_name = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    validate_error_list = validate_error_serializer(many=True)
    validate_warning_list = validate_warning_serializer(many=True)


class File_Serializer(serializers.Serializer):

    file = serializers.FileField()


class Project_Serializer(serializers.Serializer):

    project_code = serializers.CharField(allow_blank=False,allow_null=False,required=True)
    remark = serializers.CharField(allow_blank=True,allow_null=True,required=False)
    updated_by = serializers.CharField(allow_blank=False,allow_null=False,required=False)
    updated_date = serializers.DateTimeField(allow_null=True,required=False)
    customer_code = serializers.CharField(allow_blank=False,allow_null=False,required=False)
    is_active = serializers.BooleanField(required=False)

    def update(self, instance, validated_data):

        # print(validated_data)
        instance.remark = validated_data.get('remark', instance.remark)
        instance.updated_by = validated_data.get('updated_by', instance.updated_by)
        instance.customer_code = validated_data.get('customer_code', instance.customer_code)
        instance.is_active = validated_data.get('is_active', instance.customer_code)
        
        instance.updated_date =  datetime.utcnow()
        instance.save()

        return instance

    def create(self, validated_data):

        validated_data['updated_date'] = datetime.utcnow()

        return Project.objects.create(**validated_data)

class Project_Serializer_DTO(serializers.Serializer):

    serviceStatus = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    massage = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    data = Project_Serializer()

class Project_list_Serializer_DTO(serializers.Serializer):

    serviceStatus = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    massage = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    csv_name = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    data_list = Project_Serializer(many=True)



class Customer_Serializer(serializers.Serializer):

    customer_code = serializers.CharField(allow_blank=True,allow_null=True,required=False)
    station_code = serializers.CharField(allow_blank=True,allow_null=True,required=False)
    description = serializers.CharField(allow_blank=True,allow_null=True,required=False)
    station_type = serializers.CharField(allow_blank=True,allow_null=True,required=False)
    zone = serializers.CharField(allow_blank=True,allow_null=True,required=False)
    province = serializers.CharField(allow_blank=True,allow_null=True,required=False)
    address = serializers.CharField(allow_blank=True,allow_null=True,required=False)
    remark = serializers.CharField(allow_blank=True,allow_null=True,required=False)
    updated_by = serializers.CharField(allow_blank=False,allow_null=False,required=False)
    updated_date = serializers.DateTimeField(allow_null=True,required=False)
    project_code = serializers.CharField(allow_blank=True,allow_null=True,required=False)


    def update(self, instance, validated_data):

        # instance.customer_code = validated_data.get('customer_code', instance.customer_code)

        station = Station()
        station.station_code = validated_data.get('station_code', instance.station_code)
        station.description = validated_data.get('description', instance.description)
        station.station_type = validated_data.get('station_type', instance.station_type)
        station.zone = validated_data.get('zone', instance.zone)
        station.province = validated_data.get('province', instance.province)
        station.address = validated_data.get('address', instance.address)
        station.remark = validated_data.get('remark', instance.remark)
        station.updated_by = validated_data.get('updated_by', instance.updated_by)
        station.updated_date = validated_data.get('updated_date', instance.updated_date)
        station.project_code = validated_data.get('project_code', instance.project_code)
        station.is_active = validated_data.get('is_active', instance.is_active)
        station.updated_date =  datetime.utcnow()
        station.save()
        # instance.save()

        return station
        
    def create(self, validated_data):

        station = Station()
        station.station_code = validated_data.get('station_code')
        station.description = validated_data.get('description')
        station.station_type = validated_data.get('station_type')
        station.zone = validated_data.get('zone')
        station.province = validated_data.get('province')
        station.address = validated_data.get('address')
        station.remark = validated_data.get('remark')
        station.updated_by = validated_data.get('updated_by')
        station.updated_date =  datetime.utcnow()
        station.project_code = validated_data.get('project_code')
        station.is_active = True

        station.save()
        
        return station

        


class Customer_Serializer_DTO(serializers.Serializer):

    serviceStatus = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    massage = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    data = Customer_Serializer()

class Customer_list_Serializer_DTO(serializers.Serializer):

    serviceStatus = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    massage = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    csv_name = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    data_list = Customer_Serializer(many=True)



class Package_Serializer(serializers.Serializer):

    package_code = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    package_no = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    snp = serializers.IntegerField(allow_null=True,required=False)
    width = serializers.DecimalField(allow_null=True,required=False,max_digits=20, decimal_places=2)
    length = serializers.DecimalField(allow_null=True,required=False,max_digits=20, decimal_places=2)
    height = serializers.DecimalField(allow_null=True,required=False,max_digits=20, decimal_places=2)
    weight = serializers.DecimalField(allow_null=True,required=False,max_digits=20, decimal_places=2)
    station_code = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    image_url = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    updated_by = serializers.CharField(allow_blank=True,allow_null=True,required=False)
    updated_date = serializers.DateTimeField(allow_null=True,required=False)

    def update(self, instance, validated_data):

        instance.package_code = validated_data.get('package_code', instance.package_code)
        instance.snp = validated_data.get('snp', instance.snp)
        instance.width = validated_data.get('width', instance.width)
        instance.length = validated_data.get('length', instance.length)
        instance.height = validated_data.get('height', instance.height)
        instance.weight = validated_data.get('weight', instance.weight)
        instance.station_code = validated_data.get('station_code', instance.station_code)
        instance.image_url = validated_data.get('image_url', instance.image_url)
        instance.updated_date = datetime.utcnow()
        instance.save()

    def create(self, validated_data):

        return Package.objects.create(**validated_data)

class Package_Serializer_DTO(serializers.Serializer):

    serviceStatus = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    massage = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    data = Package_Serializer()

class Package_list_Serializer_DTO(serializers.Serializer):

    serviceStatus = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    massage = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    data_list = Package_Serializer(many=True)
    csv_name = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)

class Truck_Serializer(serializers.Serializer):


    truck_license = serializers.CharField(max_length=250,allow_blank=True,allow_null=True,required=False)
    province = serializers.CharField(max_length=250,allow_blank=True,allow_null=True,required=False)
    truck_type = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    fuel_type = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    max_speed = serializers.DecimalField(allow_null=True,required=False,max_digits=20, decimal_places=2)
    max_volume = serializers.DecimalField(allow_null=True,required=False,max_digits=20, decimal_places=2)
    max_weight = serializers.DecimalField(allow_null=True,required=False,max_digits=20, decimal_places=2)
    is_active = serializers.BooleanField(required=False)
    remark = serializers.CharField(max_length=500,allow_blank=True,allow_null=True,required=False)
    updated_by = serializers.CharField(allow_blank=True,allow_null=True,required=False)
    updated_date = serializers.DateTimeField(allow_null=True,required=False)


    def update(self, instance, validated_data):

        # instance.part_name = validated_data.get('part_name', instance.part_name)
        print(validated_data)
        instance.truck_license = validated_data.get('truck_license', instance.truck_license)
        instance.province = validated_data.get('province', instance.province)
        instance.truck_type = validated_data.get('truck_type', instance.truck_type)
        instance.fuel_type = validated_data.get('fuel_type', instance.fuel_type)
        instance.max_speed = validated_data.get('max_speed', instance.max_speed)
        instance.max_volume = validated_data.get('max_volume', instance.max_volume)
        instance.max_weight = validated_data.get('max_weight', instance.max_weight)
        instance.remark = validated_data.get('remark', instance.remark)
        instance.updated_date = datetime.utcnow()
        instance.save()
        return instance

    def create(self, validated_data):

        return Truck.objects.create(**validated_data)

class Truck_Serializer_DTO(serializers.Serializer):

    serviceStatus = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    massage = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    data = Truck_Serializer()

class Truck_list_Serializer_DTO(serializers.Serializer):

    serviceStatus = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    massage = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    data_list = Truck_Serializer(many=True)
    csv_name = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)


class Station_Serializer(serializers.Serializer):
 
    station_code =  serializers.CharField(max_length=250,allow_blank=False,allow_null=False,required=True)
    description = serializers.CharField(max_length=250,allow_blank=True,allow_null=True,required=False)
    station_type = serializers.CharField(max_length=250,allow_blank=True,allow_null=True,required=False)
    zone = serializers.CharField(max_length=250,allow_blank=True,allow_null=True,required=False)
    province = serializers.CharField(max_length=250,allow_blank=True,allow_null=True,required=False)
    address = serializers.CharField(max_length=250,allow_blank=True,allow_null=True,required=False)
    remark = serializers.CharField(max_length=500,allow_blank=True,allow_null=True,required=False)
    project_code = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    updated_by = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    updated_by = serializers.CharField(allow_blank=True,allow_null=True,required=False)
    updated_date = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", input_formats=['%d-%m-%Y %H:%M:%S',],allow_null=True,required=False)




class Station_list_Serializer_DTO(serializers.Serializer):

    serviceStatus = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    massage = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    data_list = Station_Serializer(many=True)

class Plant_Serializer(serializers.Serializer):
    plant_code = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)

class Plant_list_Serializer_DTO(serializers.Serializer):

    serviceStatus = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    massage = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    data_list = Plant_Serializer(many=True)


class Driver_Serializer(serializers.Serializer):

    driver_code = serializers.CharField(max_length=250,allow_blank=False,allow_null=False,required=True)
    name = serializers.CharField(max_length=250,allow_blank=True,allow_null=True,required=False)
    tel = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    remark = serializers.CharField(max_length=500,allow_blank=True,allow_null=True,required=False)
    updated_by = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    updated_date =serializers.DateTimeField(allow_null=True,required=False)

    def update(self, instance, validated_data):

        instance.name = validated_data.get('name', instance.name)
        instance.tel = validated_data.get('tel', instance.tel)
        instance.remark = validated_data.get('remark', instance.remark)
        instance.updated_date = datetime.utcnow()
        instance.save()
        return instance

    def create(self, validated_data):
        return Driver.objects.create(**validated_data)

class Driver_Serializer_DTO(serializers.Serializer):

    serviceStatus = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    massage = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    data = Driver_Serializer()

class Driver_list_Serializer_DTO(serializers.Serializer):

    serviceStatus = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    massage = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    data_list = Driver_Serializer(many=True)
    csv_name = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)




# serviceStatus = ""
#     massage = ""
#     data = object()
    


