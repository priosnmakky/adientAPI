from master_data.serializers import RouterMaster_Serializer
from model_DTO.validateError import validateError,validateErrorList
from app.helper.config.ConfigMessage import ConfigMessage
from datetime import datetime
from decimal import Decimal
from master_data.models import Customer,Project,Station
import math
import re

configMessage = ConfigMessage()
rex = re.compile("([0-2]|""){1}[0-9]{1}[.][0-5]{1}")

class RouterMasterHelper:

    validateError_obj = None
    validateError_list = []
    row_int = 0
    is_error = False

    def __init__(self):

        pass

    def validate_customer_code(self,customer_code) :

        validateError_obj =  validateError()

        if not str(customer_code) :

            validateError_obj.error = configMessage.configs.get("ROUTE_MASTER_CUSTOMERCODE_REQUIRED").data  
            validateError_obj.row = self.row_int + 1
            validateError_obj.column = 1

            self.validateError_list.append(validateError_obj)

            return None
        
        else : 
                                    
            customer_list = Customer.objects.filter(customer_code__iexact = str(customer_code))

            if len(customer_list) <=0 :
                                        
                validateError_obj.error = configMessage.configs.get("ROUTE_MASTER_CUSTOMERCODE_EXISTING").data  
                validateError_obj.row = self.row_int + 1
                validateError_obj.column = 1

                self.validateError_list.append(validateError_obj)

                return None

            else :

                return  str(customer_code)

        
    def validate_project_code(self,project_code) :

        validateError_obj =  validateError()

        if not str(project_code) :

            validateError_obj.error = configMessage.configs.get("ROUTE_MASTER_PROJECTCODE_REQUIRED").data
            validateError_obj.row = self.row_int + 1
            validateError_obj.column = 2

            self.validateError_list.append(validateError_obj)

            return None
                                
        else : 
            project_list = Project.objects.filter(project_code__iexact = str(project_code))
                                    
            if len(project_list) <=0 :

                validateError_obj.error = configMessage.configs.get("ROUTE_MASTER_PROJECTCODE_EXISTING").data
                validateError_obj.row = self.row_int + 1
                validateError_obj.column = 2

                self.validateError_list.append(validateError_obj)

                return None

            else :

                return str(project_code)

    def validate_route_code(self,route_code) :

        validateError_obj =  validateError()

        if not str(route_code) :

            validateError_obj.error = configMessage.configs.get("ROUTE_MASTER_ROUTECODE_REQUIRED").data
            validateError_obj.row = self.row_int + 1
            validateError_obj.column = 3

            self.validateError_list.append(validateError_obj)

            return None
                                
        else : 
                                    
            return str(route_code)
    
    def validate_route_trip(self,route_trip) :

        validateError_obj =  validateError()

        if not str(route_trip) :

            validateError_obj.error = configMessage.configs.get("ROUTE_MASTER_ROUTETRIP_REQUIRED").data
            validateError_obj.row = self.row_int + 1
            validateError_obj.column = 4

            self.validateError_list.append(validateError_obj)

            return None
                                
        else : 
                                    
            return str(route_trip)
    
    def validate_supplier_code(self,supplier_code) :

        validateError_obj =  validateError()

        if not str(supplier_code) :

            validateError_obj.error = configMessage.configs.get("ROUTE_MASTER_SUPPLIERCODE_REQUIRED").data
            validateError_obj.row = self.row_int + 1
            validateError_obj.column = 5

            self.validateError_list.append(validateError_obj)

            return None

        else : 
                                    
            supplier_list = Station.objects.filter(station_code__iexact=str(supplier_code).strip(),station_type__iexact="SUPPLIER",is_active=True)
            
            if len(supplier_list) <=0 :

                validateError_obj.error = configMessage.configs.get("ROUTE_MASTER_SUPPLIERCODE_EXISTING").data
                validateError_obj.row = self.row_int + 1
                validateError_obj.column = 5
                self.validateError_list.append(validateError_obj)

                return None

            else :

                return str(supplier_code)
    

    def validate_plant_code(self,plant_code) :

        validateError_obj =  validateError()

        if not str(plant_code) :

            validateError_obj.error = configMessage.configs.get("ROUTE_MASTER_PLANTCODE_REQUIRED").data
            validateError_obj.row = self.row_int + 1
            validateError_obj.column = 5

            self.validateError_list.append(validateError_obj)

            return None
                                
        else : 
                                    
            plant_list = Station.objects.filter(station_code__iexact=str(plant_code).strip(),station_type__iexact="PLANT",is_active=True)
                                    
            if len(plant_list) <=0 :

                validateError_obj.error = configMessage.configs.get("ROUTE_MASTER_PLANTCODE_EXISTING").data
                validateError_obj.row = self.row_int + 1
                validateError_obj.column = 6

                self.validateError_list.append(validateError_obj)

                return None

            else :

                return str(plant_code)
    
    def validate_pickup_before(self,pickup_before) :

        validateError_obj =  validateError()

        if  not pickup_before.isdigit() :
                                
            validateError_obj.error = configMessage.configs.get("ROUTE_MASTER_PICKUPBEFORE_INTEGER").data
            validateError_obj.row = self.row_int + 1
            validateError_obj.column = 7

            self.validateError_list.append(validateError_obj)

            return None

        else :

            return int(pickup_before)
    
    def validate_release_time(self,release_time) :

        validateError_obj =  validateError()

        if  not isinstance(release_time, int) :
    
            if rex.match(str(release_time)):

                return str(release_time)

            else:

                validateError_obj.error = configMessage.configs.get("ROUTE_MASTER_RELEASETIME_INCORRECT_FORMAT").data
                validateError_obj.row = self.row_int + 1
                validateError_obj.column = 8

                self.validateError_list.append(validateError_obj)

                return None
    
    def validate_pickup_time(self,pickup_time) :

        validateError_obj =  validateError()

        if  not isinstance(pickup_time, int) :
    
            if rex.match(str(pickup_time)):
        
                return str(pickup_time)

            else:

                validateError_obj.error = configMessage.configs.get("ROUTE_MASTER_PICKUPTIME_INCORRECT_FORMAT").data
                                    
                validateError_obj.row = self.row_int + 1
                validateError_obj.column = 9

                self.validateError_list.append(validateError_obj)

                return None
    
    def validate_depart_time(self,depart_time) :

        validateError_obj =  validateError()

        if  not isinstance(depart_time, int) :
    
            if rex.match(str(depart_time)):

                return str(depart_time)

            else:

                validateError_obj.error = configMessage.configs.get("ROUTE_MASTER_DEPARTTIME_INCORRECT_FORMAT").data
                validateError_obj.row = self.row_int + 1
                validateError_obj.column = 10

                self.validateError_list.append(validateError_obj)

                return None
    
    def validate_delivery_time(self,delivery_time) :

        validateError_obj =  validateError()

        if  not isinstance(delivery_time, int) :
    
            if rex.match(str(delivery_time)):

                return str(delivery_time)

            else:

                validateError_obj.error = configMessage.configs.get("ROUTE_MASTER_DELIVERYTIME_INCORRECT_FORMAT").data
                validateError_obj.row = self.row_int + 1
                validateError_obj.column = 11
            
                self.validateError_list.append(validateError_obj)

                return None
    
    def validate_complete_time(self,complete_time) :

        validateError_obj =  validateError()

        if  not isinstance(complete_time, int) :
    
            if rex.match(str(complete_time)):

                return str(complete_time)

            else :

                validateError_obj.error = configMessage.configs.get("ROUTE_MASTER_COMPLETETIME_INCORRECT_FORMAT").data
                validateError_obj.row = self.row_int + 1
                validateError_obj.column = 12

                self.validateError_list.append(validateError_obj)

                return None
                  
    def validate_routeMaster(self,routerMaster_list) :

        self.validateError_list = []
        self.row_int = 0

        routerMaster_return_list = []

        for routeMaster_array in routerMaster_list:

            if self.row_int > 0 :

                customer_code = self.validate_customer_code(routeMaster_array[0])

                project_code = self.validate_project_code(routeMaster_array[1])

                route_code = self.validate_route_code(routeMaster_array[2])

                route_trip = self.validate_route_trip(routeMaster_array[3])

                supplier_code = self.validate_supplier_code(routeMaster_array[4])
                
                plant_code = self.validate_plant_code(routeMaster_array[5])

                pickup_before = self.validate_pickup_before(routeMaster_array[6])

                release_time = self.validate_release_time(routeMaster_array[7])

                pickup_time = self.validate_pickup_time(routeMaster_array[8])

                depart_time = self.validate_depart_time(routeMaster_array[9])

                delivery_time = self.validate_delivery_time(routeMaster_array[10])

                complete_time = self.validate_complete_time(routeMaster_array[11])

                routerMaster_return_list.append(
                    ( 
                        project_code,route_code,
                        route_trip,supplier_code,plant_code,pickup_before,
                        release_time,pickup_time,depart_time,
                        delivery_time,complete_time
                    )
                )

            self.row_int = self.row_int + 1
            
        return routerMaster_return_list


    
    @staticmethod
    def covert_data_list_to_serializer_list(routerMaster_list) :

        routerMaster_return_list = []

        for routerMaster_obj in routerMaster_list :

            routerMaster_serializer = RouterMaster_Serializer()
            routerMaster_serializer.project_code = routerMaster_obj[0]
            routerMaster_serializer.route_no = routerMaster_obj[1]
            routerMaster_serializer.route_code = routerMaster_obj[2]
            routerMaster_serializer.route_trip = routerMaster_obj[3]
            routerMaster_serializer.supplier_code = routerMaster_obj[4]
            routerMaster_serializer.plant_code = routerMaster_obj[5]
            routerMaster_serializer.pickup_before = routerMaster_obj[6]
            routerMaster_serializer.release_time = routerMaster_obj[7]
            routerMaster_serializer.pickup_time = routerMaster_obj[8]
            routerMaster_serializer.depart_time = routerMaster_obj[9]
            routerMaster_serializer.delivery_time = routerMaster_obj[10]
            routerMaster_serializer.complete_time = routerMaster_obj[11]
            routerMaster_serializer.updated_by = routerMaster_obj[12]
            routerMaster_serializer.updated_date = routerMaster_obj[13]

            routerMaster_return_list.append(routerMaster_serializer)
        
        return routerMaster_return_list

    @staticmethod
    def formal_decimal(number_str):

        number_array = number_str.split(".")

        if len(number_array[0]) == 1 :

            number_array[0] =  "0" + number_array[0] 

        if len(number_array[1]) == 1 :

            number_array[1] =  number_array[1] +"0" 

        return number_array[0] +"."+ number_array[1]
    
    @staticmethod
    def covert_data_list_to_CSV_list(routerMaster_list) :

        routerMaster_return_list = []

        for routerMaster_obj in routerMaster_list :

            routerMaster_return_list.append([
                routerMaster_obj[0],
                routerMaster_obj[2],
                routerMaster_obj[3],
                routerMaster_obj[4],
                routerMaster_obj[5],
                routerMaster_obj[6],
                RouterMasterHelper.formal_decimal(routerMaster_obj[7]),
                RouterMasterHelper.formal_decimal(routerMaster_obj[8]),
                RouterMasterHelper.formal_decimal(routerMaster_obj[9]),
                RouterMasterHelper.formal_decimal(routerMaster_obj[10]),
                RouterMasterHelper.formal_decimal(routerMaster_obj[11]),
                routerMaster_obj[12],
                routerMaster_obj[13].strftime("%d/%m/%Y")

            ])
        
        return routerMaster_return_list
    
    

    