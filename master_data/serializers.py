from rest_framework import serializers
from master_data.models import Part,RouterMaster,Project,Customer,Package,Station,Truck,Driver,RouterInfo,CalendarMaster
from datetime import datetime, timedelta
import pandas as pd
from datetime import timezone
from master_data import views 
import re
from app.helper.config.ConfigMessage import ConfigMessage
from app.helper.file_management.FileManagement import FileManagement
configMessage = ConfigMessage()

class Part_Serializer(serializers.Serializer):

    project_code = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    supplier_code  = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    part_number = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    part_name = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    service_type = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    snp = serializers.IntegerField(allow_null=True,required=False)
    remark = serializers.CharField(max_length=250,allow_blank=True,allow_null=True,required=False)
    package_no = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    status = serializers.IntegerField(allow_null=True,required=False)
    created_by = serializers.CharField(max_length=15,allow_blank=True,allow_null=True,required=False)
    created_date = serializers.DateTimeField(allow_null=True,required=False)
    updated_by = serializers.CharField(allow_blank=True,allow_null=True,required=False)
    updated_date = serializers.DateTimeField(allow_null=True,required=False)
    package_volume = serializers.DecimalField(allow_null=True,required=False,max_digits=20, decimal_places=2)
    package_weight = serializers.DecimalField(allow_null=True,required=False,max_digits=20, decimal_places=2)

    def validate_project_code(self, project_code):

        if project_code is None or project_code.strip() == "" :

            raise serializers.ValidationError(detail=configMessage.configs.get("PART_MASTER_PROJECTCODE_REQUIRED").data)
        
        return project_code

    def validate_status(self, status):

        if status is None :

            raise serializers.ValidationError(detail=configMessage.configs.get("PART_MASTER_STATUS_REQUIRED").data)
        
        return status
    
    def validate_supplier_code(self, supplier_code):

        if supplier_code is None or supplier_code.strip()  == "":

            raise serializers.ValidationError(detail=configMessage.configs.get("PART_MASTER_SUPPLIERCODE_REQUIRED").data)
        
        return supplier_code
    
    def validate_part_number(self, part_number):

        part_list = Part.objects.filter(part_number = part_number,is_active = True)

        if part_number is None or part_number.strip()  == "":

            raise serializers.ValidationError(detail=configMessage.configs.get("PART_MASTER_PARTNUMBER_REQUIRED").data)
        
        elif not self.instance and len(part_list) > 0 :
            
            raise serializers.ValidationError(detail=configMessage.configs.get("PART_MASTER_DUPLICATE").data)

        return part_number
    
    def validate_part_name(self, part_name):

        if part_name is None or part_name.strip()  == "":

            raise serializers.ValidationError(detail=configMessage.configs.get("PART_MASTER_PARTNAME_REQUIRED").data)
        
        return part_name
    
    def validate_package_no(self, package_no):

        if package_no is None or package_no.strip()  == "":

            raise serializers.ValidationError(detail=configMessage.configs.get("PART_MASTER_PACKAGENO_REQUIRED").data)
        
        return package_no
    
    def validate_package_volume(self, package_volume):

        if package_volume is None or package_volume =='':

            raise serializers.ValidationError(detail=configMessage.configs.get("PART_MASTER_PACKAGEVOLUME_REQUIRED").data)

        return package_volume
    
    
    def validate_package_weight(self, package_weight):

        if package_weight is None or package_weight  == "" :

            raise serializers.ValidationError(detail=configMessage.configs.get("PART_MASTER_PACKAGEWEIGHT_REQUIRED").data)
        
        return package_weight


    def update(self, instance, validated_data):

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

        part_list = Part.objects.filter(part_number__iexact = validated_data.get('part_number'))

        if len(part_list) > 0:

            part_obj = part_list[0]

            part_list.update(
                package_no=validated_data['package_no'],
                package_volume=validated_data['package_volume'],
                package_weight=validated_data['package_weight'],
                remark=validated_data['remark']
            )

            return part_obj
        
        else : 

            part = Part()
            part.project_code = validated_data['project_code']
            part.status = validated_data['status']
            part.supplier_code = validated_data['supplier_code']
            part.part_number = validated_data['part_number']
            part.part_name = validated_data['part_name']
            part.package_no = validated_data['package_no']
            part.package_volume = validated_data['package_volume']
            part.package_weight = validated_data['package_weight']
            part.remark = validated_data['remark']
            part.updated_by = validated_data['updated_by']
            part.updated_date = datetime.utcnow()

            part.save()

            return part
                

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
    route_trip = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    truck_license = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    province = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    driver_code = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    driver_name = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    route_no = serializers.CharField(max_length=250,allow_blank=True,allow_null=True,required=False)
    updated_by = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    updated_date = serializers.DateTimeField(allow_null=True,required=False)

    def validate_project_code(self, project_code):

        if project_code is None or project_code.strip() == "" :
            
            raise serializers.ValidationError(detail=configMessage.configs.get("ROUTE_INFO_PROJECTCODE_REQUIRED").data)
        
        return project_code
    
    def validate_route_code(self, route_code):

        if route_code is None or route_code.strip() == "" :
            
            raise serializers.ValidationError(detail=configMessage.configs.get("ROUTE_INFO_ROUTECODE_REQUIRED").data)
        
        return route_code
    
    def validate_route_trip(self, route_trip):

        if route_trip is None or route_trip.strip() == "" :
            
            raise serializers.ValidationError(detail=configMessage.configs.get("ROUTE_INFO_ROUTETRIP_REQUIRED").data)
        
        return route_trip
    
    
    def validate_province(self, province):

        if province is None or province.strip() == "" :
            
            raise serializers.ValidationError(detail=configMessage.configs.get("ROUTE_INFO_PROVINCE_REQUIRED").data)
        
        return province
    
    def validate_truck_license(self, truck_license):

        if truck_license is None or truck_license.strip() == "" :
            
            raise serializers.ValidationError(detail=configMessage.configs.get("ROUTE_INFO_TRUCKLICENSE_REQUIRED").data)
        
        return truck_license
    
    def validate_driver_code(self, driver_code):

        if driver_code is None or driver_code.strip() == "" :
            
            raise serializers.ValidationError(detail=configMessage.configs.get("ROUTE_INFO_DRIVERCODE_REQUIRED").data)
        
        return driver_code



    def update(self, instance, validated_data):

        instance.province = validated_data.get('province', instance.province)
        instance.driver_code = validated_data.get('driver_code', instance.driver_code)
        instance.updated_by = validated_data.get('updated_by', instance.updated_by)
        instance.updated_date = datetime.utcnow()
        instance.is_active = True
        instance.save()

        return instance
    

    def create(self, validated_data):

        routerInfo = RouterInfo()
        routerInfo.project_code = validated_data['project_code']
        routerInfo.route_code = validated_data['route_code']
        routerInfo.route_trip = validated_data['route_trip']
        routerInfo.province = validated_data['province']
        routerInfo.truck_license = validated_data['truck_license']
        routerInfo.driver_code = validated_data['driver_code']
        routerInfo.updated_by = validated_data['updated_by']
        routerInfo.updated_date = datetime.utcnow()
        routerInfo.is_active = True
        
        routerInfo.save()

        return routerInfo


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
    route_trip = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
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
        
        if project_code is None or project_code.strip() == "" :

            raise serializers.ValidationError(detail=configMessage.configs.get("ROUTE_MASTER_PROJECTCODE_REQUIRED").data)
        
        return project_code

    def validate_route_code(self, route_code):

        if route_code is None or route_code.strip() == "" :

            raise serializers.ValidationError(detail=configMessage.configs.get("ROUTE_MASTER_ROUTECODE_REQUIRED").data)
        
        return route_code
    
    def validate_route_trip(self, route_trip):

        if route_trip is None or route_trip.strip() == "" :

            raise serializers.ValidationError(detail=configMessage.configs.get("ROUTE_MASTER_TRIPNO_REQUIRED").data)
        
        return route_trip
    
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
    
    def validate(self, data):

        routerMaster_list = RouterMaster.objects.filter(
            route_code = data['route_code'],
            route_trip = data['route_trip'],
            supplier_code = data['supplier_code'],
            plant_code = data['plant_code'],
            is_active=True
            )

        if not self.instance and len(routerMaster_list) > 0 :

            raise serializers.ValidationError(detail=configMessage.configs.get("ROUTE_MASTER_DUPLICATE").data)


        return data
    
    

    def update(self, instance, validated_data):

      
        instance.pickup_before = validated_data.get('pickup_before', instance.pickup_before)
        instance.release_time = validated_data.get('release_time', instance.release_time)
        instance.pickup_time = validated_data.get('pickup_time', instance.pickup_time)
        instance.depart_time = validated_data.get('depart_time', instance.depart_time)
        instance.delivery_time = validated_data.get('delivery_time', instance.delivery_time)
        instance.complete_time = validated_data.get('complete_time', instance.complete_time)
        instance.updated_by = validated_data.get('updated_by', instance.updated_by)
        instance.updated_date = datetime.utcnow()
        instance.is_active = True
        instance.save()

        return instance

    def create(self, validated_data):
      
        routerMaster_list = RouterMaster.objects.filter(route_code = validated_data['route_code'],
            route_trip = validated_data['route_trip'],
            supplier_code = validated_data['supplier_code'],
            plant_code = validated_data['plant_code'])

        if len(routerMaster_list) > 0:

            routerMaster_obj = routerMaster_list[0]

            routerMaster_list.update(
                pickup_before=validated_data['pickup_before'],
                release_time=validated_data['release_time'],
                pickup_time=validated_data['pickup_time'],
                depart_time=validated_data['depart_time'],
                delivery_time=validated_data['delivery_time'],
                complete_time=validated_data['complete_time'],
                is_active=True
            )

            return routerMaster_obj
        
        else : 

            routerMaster = RouterMaster()

            routerMaster.project_code = validated_data['project_code']
            routerMaster.route_no = validated_data['route_code'].upper()+ "-" + validated_data['route_trip'].upper() + "-" + validated_data['supplier_code'].upper() + "-" + validated_data['plant_code'].upper()
            routerMaster.route_code = validated_data['route_code']
            routerMaster.route_trip = validated_data['route_trip']
            routerMaster.supplier_code = validated_data['supplier_code']
            routerMaster.plant_code = validated_data['plant_code']
            routerMaster.pickup_before = validated_data['pickup_before']
            routerMaster.release_time = validated_data['release_time']
            routerMaster.pickup_time = validated_data['pickup_time']
            routerMaster.depart_time = validated_data['depart_time']
            routerMaster.delivery_time = validated_data['delivery_time']
            routerMaster.complete_time = validated_data['complete_time']
            routerMaster.updated_by = validated_data['updated_by']
            routerMaster.updated_date = datetime.utcnow()

            routerMaster.is_active = True

            routerMaster.save()

            return routerMaster

    
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

    project_code = serializers.CharField(allow_blank=True,allow_null=True,required=True)
    remark = serializers.CharField(allow_blank=True,allow_null=True,required=False)
    updated_by = serializers.CharField(allow_blank=False,allow_null=False,required=False)
    updated_date = serializers.DateTimeField(allow_null=True,required=False)
    customer_code = serializers.CharField(allow_blank=True,allow_null=True,required=True)
    is_active = serializers.BooleanField(required=False)

    def validate_project_code(self, project_code):

        project_list =  Project.objects.filter(project_code__iexact = project_code,is_active=True)

        if project_code is None or project_code.strip() == "" :

            raise serializers.ValidationError(detail=configMessage.configs.get("PROJECT_MASTER_PROJECT_REQUIRED").data)
        
        if not self.instance and len(project_list) > 0:

            raise serializers.ValidationError(detail=configMessage.configs.get("PROJECT_MASTER_DUPLICATE").data)
         
        return project_code
    
    def validate_customer_code(self,customer_code):

        if customer_code is None or customer_code.strip() == "" :

            raise serializers.ValidationError(detail=configMessage.configs.get("PROJECT_MASTER_CUSTOMER_REQUIRED").data)
        
        return customer_code
    
    def validate(self,project_validate):

        return project_validate

    def update(self, instance, validated_data):

        instance.remark = validated_data.get('remark', instance.remark)
        instance.customer_code= validated_data.get('customer_code', instance.customer_code)
        instance.is_active=True 
        instance.updated_date =  datetime.utcnow()
        instance.save()
        return instance

    def create(self, validated_data):

        project_list =  Project.objects.filter(project_code__iexact = validated_data['project_code'],is_active=False)

        if len(project_list) > 0 :

            project_obj = project_list[0]

            project_list.update(
                customer_code= validated_data['customer_code'],
                remark= validated_data['remark'],
                is_active=True
            )
            
            return project_obj
        else : 

            project_obj =  Project()
            project_obj.project_code = validated_data['project_code']
            project_obj.customer_code = validated_data['customer_code']
            project_obj.remark = validated_data['remark']
            project_obj.updated_date = datetime.utcnow()
            project_obj.updated_by = validated_data['updated_by']
            project_obj.is_active = True

            return project_obj

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


    project_code = serializers.CharField(allow_blank=True,allow_null=True,required=False)
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

    def validate_project_code(self,project_code):

        if project_code is None or project_code.strip() == "" :

            raise serializers.ValidationError(detail=configMessage.configs.get("STATION_MASTER_PROJECT_REQUIRED").data)
        
        return project_code
    
    def validate_station_code(self,station_code):

        station_list = Station.objects.filter(station_code__iexact = station_code,is_active=True)

        if station_code is None or station_code.strip() == "" :

            raise serializers.ValidationError(detail=configMessage.configs.get("STATION_MASTER_STATIONCODE_REQUIRED").data)
        
        if not self.instance and len(station_list) > 0:

            raise serializers.ValidationError(detail=configMessage.configs.get("STATION_MASTER_DUPLICATE").data)
         
        return station_code
    
    def validate_description(self,description):

        if description is None or description.strip() == "" :

            raise serializers.ValidationError(detail=configMessage.configs.get("STATION_MASTER_DESCRIPTION_REQUIRED").data)
        
        return description
    
    def validate_station_type(self,station_type):

        if station_type is None or station_type.strip() == "" :

            raise serializers.ValidationError(detail=configMessage.configs.get("STATION_MASTER_TYPE_REQUIRED").data)
        
        return station_type
    
    def validate_zone(self,zone):

        if zone is None or zone.strip() == "" :

            raise serializers.ValidationError(detail=configMessage.configs.get("STATION_MASTER_ZONE_REQUIRED").data)
        
        return zone
    
    def validate_province(self,province):

        if province is None or province.strip() == "" :

            raise serializers.ValidationError(detail=configMessage.configs.get("STATION_MASTER_PROVINCE_REQUIRED").data)
        
        return province
    
    def validate_address(self,address):

        if address is None or address.strip() == "" :

            raise serializers.ValidationError(detail=configMessage.configs.get("STATION_MASTER_ADDRESS_REQUIRED").data)
        
        return address

    def create_calendarMaster(self,station_code,updated_by) :

        start_date = datetime(datetime.now().year+1, 1, 1)
        end_date = datetime(datetime.now().year+1, 12, 31)
        daterange = pd.date_range(start_date, end_date)
        for single_date in daterange:

            calendarMaster_obj =  CalendarMaster()
            calendarMaster_obj.plant_code = station_code
            day_int = int(single_date.strftime("%w")) + 1
            calendarMaster_obj.day = day_int
            calendarMaster_obj.date = single_date
                            
            if day_int == 1 :

                calendarMaster_obj.is_working =  False 
                            
            else : 

                calendarMaster_obj.is_working = True
                            
            calendarMaster_obj.updated_by = updated_by
            calendarMaster_obj.updated_date = datetime.utcnow()
            calendarMaster_obj.is_active = True

            calendarMaster_obj.save()

        return calendarMaster_obj



    def update(self, station, validated_data):

        calendarMaster_list = CalendarMaster.objects.filter(plant_code__iexact=validated_data.get('station_code', station.station_code))
        if len(calendarMaster_list) > 0 and validated_data.get('station_type', station.station_type) == 'SUPPLIER' :

            calendarMaster_list.update(is_active = False)
            
        if len(calendarMaster_list) == 0 and validated_data.get('station_type', station.station_type) == 'PLANT':

            self.create_calendarMaster(validated_data.get('station_code', station.station_code),validated_data.get('updated_by', station.updated_by))
      
        station.project_code = validated_data.get('project_code', station.project_code)
        station.station_code = validated_data.get('station_code', station.station_code)
        station.description = validated_data.get('description', station.description)
        station.station_type = validated_data.get('station_type', station.station_type)
        station.zone = validated_data.get('zone', station.zone)
        station.province = validated_data.get('province', station.province)
        station.address = validated_data.get('address', station.address)
        station.remark = validated_data.get('remark', station.remark)
        station.updated_by = validated_data.get('updated_by', station.updated_by)
        station.updated_date = validated_data.get('updated_date', station.updated_date)
        station.is_active = True
        station.updated_date =  datetime.utcnow()
        station.save()
        
        return station

    def create(self, validated_data):

        station_list =  Station.objects.filter(station_code__iexact = validated_data['station_code'],is_active=False)

        if len(station_list) > 0 :

            station_obj = station_list[0]

            station_list.update(
                description= validated_data['description'],
                station_type= validated_data['station_type'],
                zone= validated_data['zone'],
                province= validated_data['province'],
                address= validated_data['address'],
                remark= validated_data['remark'],
                project_code= validated_data['project_code'],
                updated_by = validated_data['updated_by'],
                updated_date = datetime.utcnow(),
                is_active=True
            )
            
            return station_obj
        else : 

            station = Station()
            station.project_code = validated_data.get('project_code')
            station.station_code = validated_data.get('station_code')
            station.description = validated_data.get('description')
            station.station_type = validated_data.get('station_type')
            station.zone = validated_data.get('zone')
            station.province = validated_data.get('province')
            station.address = validated_data.get('address')
            station.remark = validated_data.get('remark')
            station.updated_by = validated_data.get('updated_by')
            station.updated_date =  datetime.utcnow()
            station.is_active = True

            station.save()
        
            if validated_data.get('station_type') == "PLANT":

                self.create_calendarMaster(validated_data.get('station_code'),validated_data.get('updated_by'))

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
 

    def validate_station_code(self,station_code):

        if station_code == "null" or station_code == "" :

            raise serializers.ValidationError(detail=configMessage.configs.get("PACKAGES_MASTER_STATIONCODE_REQUIRED").data)
        
        return station_code

    def validate_package_code(self,package_code):

        if package_code == "null" or package_code == "" :

            raise serializers.ValidationError(detail=configMessage.configs.get("PACKAGES_MASTER_PACKAGECODE_REQUIRED").data)
        
        return package_code

    def validate_package_no(self,package_no):

        package_list = Package.objects.filter(detail=request.POST['package_no'],is_active=True)

        if package_no == "null" or package_no == "" :

            raise serializers.ValidationError(detail=configMessage.configs.get("PACKAGES_MASTER_PACKAGENO_REQUIRED").data)
        
        elif  len(package_list) > 0 :

            raise serializers.ValidationError(detail=configMessage.configs.get("PACKAGES_MASTER_DUPLICATE").data)

        return package_no
    
    def validate_snp(self,snp):

        if snp == "null" or snp == "" :

            raise serializers.ValidationError(detail=configMessage.configs.get("PACKAGES_MASTER_SNP_REQUIRED").data)
        
        elif snp <= 0 :

            raise serializers.ValidationError(detail=configMessage.configs.get("PACKAGES_MASTER_SNP_MORE_THAN_ZERO").data)

        return snp
    
    def validate_width(self,width):

        if width == "null" or width == "" :

            raise serializers.ValidationError(detail=configMessage.configs.get("PACKAGES_MASTER_WIDTH_REQUIRED").data)
        
        return width
    
    def validate_length(self,length):

        if length == "null" or length == "" :

            raise serializers.ValidationError(detail=configMessage.configs.get("PACKAGES_MASTER_LENGTH_REQUIRED").data)
        
        return length

    def validate_height(self,height):

        if height == "null" or height == "" :

            raise serializers.ValidationError(detail=configMessage.configs.get("PACKAGES_MASTER_HEIGHT_REQUIRED").data)
        
        return height
    
    def validate_weight(self,weight):

        if weight == "null" or weight == "" :

            raise serializers.ValidationError(detail=configMessage.configs.get("PACKAGES_MASTER_WEIGHT_REQUIRED").data)
        
        return weight
    

    

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

        return instance

    def create(self, validated_data):

        
        package_list =  Package.objects.filter(package_no = validated_data.get('package_no'),is_active=False)

        if len(package_list) > 0 :

            package_obj = package_list[0]

            package_list.update(
                snp= validated_data['snp'],
                width= validated_data['width'],
                length= validated_data['length'],
                height= validated_data['height'],
                weight= validated_data['weight'],
                image_url= validated_data['image_url'],
                updated_by = validated_data['updated_by'],
                updated_date = datetime.utcnow(),
                is_active=True
            )

            return package_obj
        
        else : 
            
            package = Package()
            package.package_code = validated_data.get('package_code')
            package.package_no = validated_data.get('package_no')
            package.snp = validated_data.get('snp')
            package.width = validated_data.get('width')
            package.length = validated_data.get('length')
            package.height = validated_data.get('height')
            package.weight = validated_data.get('weight')
            package.station_code = validated_data.get('station_code')
            package.image_url = validated_data.get('image_url')
            package.updated_by = validated_data.get('updated_by')
            package.updated_date = datetime.utcnow()
            package.is_active = True

            return package

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

    def validate_truck_license(self, truck_license):

        truck_list = Truck.objects.filter(truck_license= truck_license,is_active= True)
        
        if truck_license is None or truck_license  == "" :

            raise serializers.ValidationError(detail=configMessage.configs.get("TRUCK_MASTER_TRUCKLICENSE_REQUIRED").data)
        
        elif not self.instance and len(truck_list) > 0 :

            raise serializers.ValidationError(detail=configMessage.configs.get("TRUCK_MASTER_DUPLICATE").data)

        return truck_license
    
    def validate_province(self, province):

        if province is None or province  == "" :

            raise serializers.ValidationError(detail=configMessage.configs.get("TRUCK_MASTER_PROVINCE_REQUIRED").data)
        
        return province
    
    def validate_truck_type(self, truck_type):

        if truck_type is None or truck_type  == "" :

            raise serializers.ValidationError(detail=configMessage.configs.get("TRUCK_MASTER_TRUCKTYPE_REQUIRED").data)
        
        return truck_type
    
    def validate_fuel_type(self, fuel_type):

        if fuel_type is None or fuel_type  == "" :

            raise serializers.ValidationError(detail=configMessage.configs.get("TRUCK_MASTER_FUELTYPE_REQUIRED").data)
        
        return fuel_type
    
    def validate_max_speed(self, max_speed):

        if max_speed is None or max_speed  == "" :

            raise serializers.ValidationError(detail=configMessage.configs.get("TRUCK_MASTER_MAXSPEED_REQUIRED").data)
        
        return max_speed
    
    def validate_max_volume(self, max_volume):

        if max_volume is None or max_volume  == "" :

            raise serializers.ValidationError(detail=configMessage.configs.get("TRUCK_MASTER_MAXVOLUME_REQUIRED").data)
        
        return max_volume
    
    def validate_max_weight(self, max_weight):

        if max_weight is None or max_weight  == "" :

            raise serializers.ValidationError(detail=configMessage.configs.get("TRUCK_MASTER_MAXWEIGHT_REQUIRED").data)
        
        return max_weight
  

    def update(self, instance, validated_data):

    
        instance.province = validated_data.get('province', instance.province)
        instance.truck_type = validated_data.get('truck_type', instance.truck_type)
        instance.fuel_type = validated_data.get('fuel_type', instance.fuel_type)
        instance.max_speed = validated_data.get('max_speed', instance.max_speed)
        instance.max_volume = validated_data.get('max_volume', instance.max_volume)
        instance.max_weight = validated_data.get('max_weight', instance.max_weight)
        instance.remark = validated_data.get('remark', instance.remark)
        instance.is_active = True
        instance.updated_date = datetime.utcnow()

        instance.save()

        return instance

    def create(self, validated_data):

        truck_list = Truck.objects.filter(truck_license = validated_data['truck_license'])

        if len(truck_list) > 0:

            truck_obj = truck_list[0]

            truck_list.update(
                province=validated_data['province'],
                truck_type=validated_data['truck_type'],
                fuel_type=validated_data['fuel_type'],
                max_speed=validated_data['max_speed'],
                max_volume=validated_data['max_volume'],
                max_weight=validated_data['max_weight'],
                remark=validated_data['max_weight'],
                is_active=True
            )

            return truck_obj
        
        else : 

            truck = Truck()
            truck.truck_license = validated_data['truck_license']
            truck.province = validated_data['province']
            truck.truck_type = validated_data['truck_type']
            truck.fuel_type = validated_data['fuel_type']
            truck.max_speed = validated_data['max_speed']
            truck.max_volume = validated_data['max_volume']
            truck.max_weight = validated_data['max_weight']
            truck.remark = validated_data['remark']
            truck.updated_by = validated_data['updated_by']
            truck.updated_date = datetime.utcnow()

            truck.save()

            return truck


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

    driver_code = serializers.CharField(max_length=250,allow_blank=True,allow_null=True,required=True)
    name = serializers.CharField(max_length=250,allow_blank=True,allow_null=True,required=False)
    tel = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    remark = serializers.CharField(max_length=500,allow_blank=True,allow_null=True,required=False)
    updated_by = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    updated_date =serializers.DateTimeField(allow_null=True,required=False)

    def validate_driver_code(self, driver_code):

        driver_list = Driver.objects.filter(driver_code__iexact=driver_code,is_active= True)
        
        if driver_code is None or driver_code.strip()  == "" :

            raise serializers.ValidationError(detail=configMessage.configs.get("DRIVER_MASTER_DRIVERCODE_REQUIRED").data)
        
        elif not self.instance and len(driver_list) > 0 :

            raise serializers.ValidationError(detail=configMessage.configs.get("DRIVER_MASTER_DUPLICATE").data)

        return driver_code
    
    def validate_name(self, name):

        if name is None or name.strip()  == "" :

            raise serializers.ValidationError(detail=configMessage.configs.get("DRIVER_MASTER_DRIVERNAME_REQUIRED").data)
        
        return name
    
    def validate_tel(self, tel):

        if tel is None or tel.strip()  == "" :

            raise serializers.ValidationError(detail=configMessage.configs.get("DRIVER_MASTER_DRIVERTEL_REQUIRED").data)
        
        return tel

    def update(self, instance, validated_data):

        instance.name = validated_data.get('name', instance.name)
        instance.tel = validated_data.get('tel', instance.tel)
        instance.remark = validated_data.get('remark', instance.remark)
        instance.is_active = True
        instance.updated_date = datetime.utcnow()

        instance.save()

        return instance

    def create(self, validated_data):

        driver_list = Driver.objects.filter( driver_code= validated_data['driver_code'])

        if len(driver_list) > 0:

            driver_obj = driver_list[0]

            driver_list.update(
                name=validated_data['name'],
                tel=validated_data['tel'],
                remark=validated_data['remark'],
                is_active=True
            )

            return driver_obj
        
        else : 

            driver = Driver()
            driver.driver_code = validated_data['driver_code']
            driver.name = validated_data['name']
            driver.tel = validated_data['tel']
            driver.remark = validated_data['remark']
            driver.updated_by = validated_data['updated_by']
            driver.updated_date = datetime.utcnow()
            driver.is_active = True

            driver.save()

            return driver


class Driver_Serializer_DTO(serializers.Serializer):

    serviceStatus = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    massage = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    data = Driver_Serializer()

class Driver_list_Serializer_DTO(serializers.Serializer):

    serviceStatus = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    massage = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    data_list = Driver_Serializer(many=True)
    csv_name = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)



