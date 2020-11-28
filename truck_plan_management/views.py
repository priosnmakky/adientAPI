from django.shortcuts import render
from order.models import File,Order
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from app.services.truck_plan_management.TruckPlanManagementService import TruckPlanManagementService
from app.serializersMapping.SerializerMapping import SerializerMapping
from order.serializers import OrderSerializer,Order_list_Serializer_DTO
from master_data.serializers import RouterMaster_Serializer,RouterMaster_Serializer_DTO,RouterMaster_list_Serializer_DTO
from truck_plan_management.serializers import PickUp_Serializer,PickUp_Serializer_DTO,PickUp_list_Serializer_DTO
from truck_plan_management.serializers import TruckPlan_Serializer,TruckPlan_Serializer_DTO,TruckPlan_list_Serializer_DTO
from django.http.response import JsonResponse
from truck_plan_management.models import PickUp,TruckPlan
from app.helper.generate_PUS.Generate_PUS import Genetate_PUS
from datetime import datetime
from app.helper.error_helper.ErrorHelper import ErrorHelper
from app.helper.config.ConfigMessage import ConfigMessage
from app.helper.CSV_file_management.CSVFileManagement import CSVFileManagement
from django.db.models import Q
from rest_framework.response import Response
from app.helper.pickup_gen_helper.PickupGenHelper import PickupGenHelper
from app.helper.pickup_print_helper.PickupPrintHelper import PickupPrintHelper
from app.helper.truckplan_gen_helper.TruckGenHelper import TruckGenHelper
from app.helper.truckplan_print_helper.TruckplanPrintHelper import TruckplanPrintHelper

configMessage = ConfigMessage()


truckPlanManagementService = TruckPlanManagementService()
serializerMapping = SerializerMapping()

@api_view(['GET', 'POST'])
def search_order_for_generate_pickup(request):

    if request.method == 'POST':

        try:

            pickup_data = JSONParser().parse(request)

            customer_code = pickup_data['customer_code_selected']
            project_code = pickup_data['project_code_selected']
            due_date = pickup_data['due_date_selected']

            pickup_list =  truckPlanManagementService.search_generate_pickup(
                customer_code,
                project_code,
                due_date
                )

            pickup_list = PickupGenHelper.covert_data_list_to_serializer_list(pickup_list)

            serializer = serializerMapping.mapping_serializer_list(
                Order_list_Serializer_DTO,
                pickup_list,
                "success", 
                None,
                "",
                None,
                None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)
    

        except Exception as e:

            serializer = serializerMapping.mapping_serializer_list(
                    Order_list_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def search_and_print_PUS(request):

    if request.method == 'POST':

        try:

            search_and_print_PUS_obj = JSONParser().parse(request)

            customer_code = search_and_print_PUS_obj['customer_code_selected']
            project_code = search_and_print_PUS_obj['project_code_selected']
            supplier_code = search_and_print_PUS_obj['supplier_code_selected']
            due_date_from = search_and_print_PUS_obj['due_date_from_selected']
            due_date_to = search_and_print_PUS_obj['due_date_to_selected']
            PUS_ref = search_and_print_PUS_obj['PUS_ref_selected']

            pickUp_list = truckPlanManagementService.search_pickUp_PUS(
                customer_code,
                project_code,
                supplier_code,
                due_date_from,
                due_date_to,
                PUS_ref
                )
            
            name_csv_str = "SearchAndPrintPUSCSV_" +datetime.now().strftime("%Y%m%d_%H%M%S")
            CSV_file_management_obj = CSVFileManagement(name_csv_str,"media/",'',',')
            CSV_file_management_obj.covert_to_header([
               "PUS Ref","Status","Supplier","Plant",
               "Order Count","Due Date",
               "Release Time","Delivery Time",
               "Route Code","Trip","Truck License",
               "Driver Name"])
   
            pickUp_CSV_list = PickupPrintHelper.covert_data_list_to_CSV_list(pickUp_list)
            CSV_file_management_obj.covert_to_CSV_data_list(pickUp_CSV_list)
            return_name_CSV_str = CSV_file_management_obj.genearete_CSV_file()
            serializer_list =  PickupPrintHelper.covert_data_list_to_serializer_list(pickUp_list)

            serializer = serializerMapping.mapping_serializer_list(
                PickUp_list_Serializer_DTO,
                serializer_list,
                "success", 
                "",
                name_csv_str + '.csv',
                None,
                None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            

            serializer = serializerMapping.mapping_serializer_list(
                    PickUp_list_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)
 
       

@api_view(['GET', 'POST'])
def generate_PUS(request):

    if request.method == 'POST':

        try:

            pickUp_list = JSONParser().parse(request)['orderList']
            
            print(pickUp_list)
            # for pickUp_obj in pickUp_list :

            #     pickUp_obj['due_date'] = datetime.strptimepickUp_obj(['due_date'], "%d/%m/%Y")

            pickUp_serializer = PickUp_Serializer(data=pickUp_list,many = True)
    
            if pickUp_serializer.is_valid():
                print(pickUp_list)
                pickUp_obj =  pickUp_serializer.save(is_active=True,updated_by=request.user.username,updated_date=datetime.utcnow())

                serializer = serializerMapping.mapping_serializer_list(
                    PickUp_Serializer_DTO,
                    pickUp_obj,
                    "success", 
                    configMessage.configs.get("STATION_MASTER_DELETE_MASSAGE_SUCCESSFUL").data,
                    "",
                    None,
                    None )
            
            else :

                serializer = serializerMapping.mapping_serializer_obj(
                    PickUp_Serializer_DTO,
                    None,
                    "Error",
                    ErrorHelper.get_error_massage(pickUp_serializer.errors),
                    None,
                    None,
                    None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)
                
        except Exception as e:

            serializer = serializerMapping.mapping_serializer_obj(
                    PickUp_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)    





@api_view(['GET', 'POST'])
def create_route(request):

    if request.method == 'POST':

        try:

            pickup_data = JSONParser().parse(request)
            routerMaster_data = pickup_data['routeMaster']
            routerMaster_serializer_obj = RouterMaster_Serializer(data=routerMaster_data)

            if routerMaster_serializer_obj.is_valid():

                routerMaster_obj = routerMaster_serializer_obj.save()

                

                pickUp_data = {
                    'supplier_code':routerMaster_obj.supplier_code, 
                    'plant_code':routerMaster_obj.plant_code,
                    'due_date':pickup_data['add_due_date'],
                    'route_code':routerMaster_obj.route_code,
                    'route_trip':routerMaster_obj.route_trip,
                    'updated_by':routerMaster_obj.updated_by,
                    'updated_date':routerMaster_obj.updated_date,
                        }

                pickUp_serializer = PickUp_Serializer(data=pickUp_data )

                if pickUp_serializer.is_valid():

                    pickUp_obj = pickUp_serializer.save() 
                    serializer = serializerMapping.mapping_serializer_obj(
                        PickUp_Serializer_DTO,
                        pickUp_obj,
                        "success", 
                        configMessage.configs.get("GENERATEP_PUS_MANUAL_MASSAGE_SUCCESSFUL").data,
                        "",
                        None,
                        None )
                else :

                    serializer = serializerMapping.mapping_serializer_obj(
                        PickUp_Serializer_DTO,
                        None,
                        "Error",
                        ErrorHelper.get_error_massage(pickUp_serializer.errors),
                        None,
                        None,
                        None )


            else :

                serializer = serializerMapping.mapping_serializer_obj(
                    PickUp_Serializer_DTO,
                    None,
                    "Error",
                    ErrorHelper.get_error_massage(routerMaster_serializer_obj.errors),
                    None,
                    None,
                    None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:

            serializer = serializerMapping.mapping_serializer_obj(
                PickUp_Serializer_DTO,
                None,
                "Error",
                e,
                None,
                None,
                None )
                
            return Response(serializer.data, status=status.HTTP_200_OK)



@api_view([ 'POST'])
def get_order_by_pickup_no(request):

    if request.method == 'POST':

        try:

            pickup_data = JSONParser().parse(request)
            pickup_obj = PickUp.objects.filter(pickup_no= pickup_data['pickup_no'])[0]
            order_list = Order.objects.filter(
                            supplier_code=pickup_obj.supplier_code,
                            plant_code=pickup_obj.plant_code,
                            due_date__year=pickup_obj.due_date.year,
                            due_date__month=pickup_obj.due_date.month,
                            due_date__day=pickup_obj.due_date.day,
                            route_code=pickup_obj.route_code,
                            route_trip=pickup_obj.route_trip,
                            is_route_completed=True,
                            is_part_completed=True,
                            is_deleted=False
                            )
            
            order_serializer =  OrderSerializer(order_list,many=True)

            serializer = serializerMapping.mapping_serializer_list(
                        Order_list_Serializer_DTO,
                        order_serializer.data,
                        "success", 
                        None,
                        "",
                        None,
                        None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:

            serializer = serializerMapping.mapping_serializer_list(
                Order_list_Serializer_DTO,
                None,
                "Error",
                e,
                None,
                None,
                None )
                
            return Response(serializer.data, status=status.HTTP_200_OK)

@api_view([ 'POST'])
def deleted_order_in_pickup(request):

    if request.method == 'POST':

        try:

            order_data = JSONParser().parse(request)
            order_list = Order.objects.filter(order_no= order_data['order_no'])
            order_list.update(pickup_no="")


            serializer = serializerMapping.mapping_serializer_listorder_list(
                Order_list_Serializer_DTO,
                order_list,
                "success", 
                None,
                "",
                None,
                None )

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:

            serializer = serializerMapping.mapping_serializer_list(
                Order_list_Serializer_DTO,
                None,
                "Error",
                e,
                None,
                None,
                None )
                
            return Response(serializer.data, status=status.HTTP_200_OK)
        

@api_view([ 'POST'])
def add_order_in_pickup(request):

    if request.method == 'POST':

        try:
            
            order_data = JSONParser().parse(request)
            order_list = Order.objects.filter(order_no= order_data['order_no'])
            order_list.update(pickup_no=order_data['pickup_no'])

            pickUp_list = PickUp.objects.filter(pickup_no=order_data['pickup_no'])
            pickUp_list.update(status=2)

            serializer = serializerMapping.mapping_serializer_list(
                Order_list_Serializer_DTO,
                order_list,
                "success", 
                None,
                "",
                None,
                None )

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:

            serializer = serializerMapping.mapping_serializer_list(
                Order_list_Serializer_DTO,
                None,
                "Error",
                e,
                None,
                None,
                None )
                
            return Response(serializer.data, status=status.HTTP_200_OK)

@api_view([ 'POST'])
def delete_pickUp(request):

    if request.method == 'POST':

        try:

            pickUp_data = JSONParser().parse(request)
            pickUp_list = PickUp.objects.filter(pickup_no=pickUp_data['pickup_no'])
            pickUp_list.update(status=1)

            order_list = Order.objects.filter(pickup_no=pickUp_data['pickup_no'])
            order_list.update(pickup_no="")

            serializer = serializerMapping.mapping_serializer_list(
                Order_list_Serializer_DTO,
                order_list,
                "success", 
                None,
                "",
                None,
                None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:

            serializer = serializerMapping.mapping_serializer_list(
                Order_list_Serializer_DTO,
                None,
                "Error",
                e,
                None,
                None,
                None )
                
            return Response(serializer.data, status=status.HTTP_200_OK)
     
@api_view([ 'POST'])
def delete_truckplan(request):

    if request.method == 'POST':

        try:

            truckPlan_data = JSONParser().parse(request)
            truckPlan_list = TruckPlan.objects.filter(truckplan_no=truckPlan_data['truckplan_no'])
            truckPlan_list.update(status=1)

            pickUp_list = PickUp.objects.filter(truckplan_no=truckPlan_data['truckplan_no'])
            pickUp_list.update(truckplan_no="")

            pickUp_Serializer =  PickUp_Serializer(pickUp_list,many = True)

            serializer = serializerMapping.mapping_serializer_list(
                PickUp_list_Serializer_DTO,
                pickUp_Serializer.data,
                "success", 
                None,
                "",
                None,
                None )

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:

            serializer = serializerMapping.mapping_serializer_list(
                    PickUp_list_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)

        # try:
   
        #     truckPlan_data = JSONParser().parse(request)

        #     truckPlan_list = TruckPlan.objects.filter(truckplan_no=truckPlan_data['truckplan_no'])
        #     truckPlan_list.update(status=1)

        #     pickUp_list = PickUp.objects.filter(truckplan_no=truckPlan_data['truckplan_no'])

        #     pickUp_list.update(truckplan_no="")

        #     pickUp_Serializer =  PickUp_Serializer(pickUp_list)
     
        #     pickUp_list_serializer_DTO = serializerMapping.mapping_list_successful(
        #                 pickUp_Serializer.data,
        #                 PickUp_list_Serializer_DTO,
        #                 "",
        #                 None)
            
        #     return JsonResponse(pickUp_list_serializer_DTO.data, status=status.HTTP_200_OK)
       
        # except Exception as e:

        #     pickUp_serializer_error_DTO = serializerMapping.mapping_obj_error(PickUp_list_Serializer_DTO,e)

        #     return JsonResponse(pickUp_serializer_error_DTO.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def search_generate_truck_plan(request):

    if request.method == 'POST':

        try:

            truckplan_data = JSONParser().parse(request)

            customer_code = truckplan_data['customer_code_selected']
            project_code = truckplan_data['project_code_selected']
            due_date = truckplan_data['due_date_to_selected']

            truckplan_list = truckPlanManagementService.search_generate_truck_plan(
                customer_code,
                project_code,
                due_date
                )
            
            truckplan_list = TruckGenHelper.covert_data_list_to_serializer_list(truckplan_list)

            serializer = serializerMapping.mapping_serializer_list(
                TruckPlan_list_Serializer_DTO,
                truckplan_list,
                "success", 
                None,
                "",
                None,
                None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:

            serializer = serializerMapping.mapping_serializer_list(
                    TruckPlan_list_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)
            
      

@api_view(['GET', 'POST'])
def generate_truck_plan(request):

    if request.method == 'POST':

        try:

            truckPlant_list = JSONParser().parse(request)['orderPickList']
            
            truckplan_serializer = TruckPlan_Serializer(data=truckPlant_list,many = True)

            if truckplan_serializer.is_valid():
                
                truckplan_serializer.save(is_active=True,updated_by=request.user.username,updated_date=datetime.utcnow())

                serializer = serializerMapping.mapping_serializer_list(
                    TruckPlan_list_Serializer_DTO,
                    truckplan_serializer.data,
                    "success", 
                    None,
                    "",
                    None,
                    None )
            
            else :

                serializer = serializerMapping.mapping_serializer_list(
                    TruckPlan_list_Serializer_DTO,
                    None,
                    "Error",
                    ErrorHelper.get_error_massage(truckplan_serializer.errors),
                    None,
                    None,
                    None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:

            serializer = serializerMapping.mapping_serializer_list(
                    TruckPlan_list_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def search_and_print_truck_plan(request):

    if request.method == 'POST':

        try:

            search_and_print_truck_plan_obj = JSONParser().parse(request)
            customer_code = search_and_print_truck_plan_obj['customer_code_selected']
            project_code = search_and_print_truck_plan_obj['project_code_selected']
            due_date_from = search_and_print_truck_plan_obj['due_date_from_selected']
            due_date_to = search_and_print_truck_plan_obj['due_date_to_selected']
            truck_plan_ref = search_and_print_truck_plan_obj['truck_plan_ref']

            truckplan_list = truckPlanManagementService.search_and_print_truck_plan(
                customer_code,
                project_code,
                due_date_from,
                due_date_to,
                truck_plan_ref
                )
            
            name_csv_str = "SearchAndPrintTruckPlanCSV_" +datetime.now().strftime("%Y%m%d_%H%M%S")
            CSV_file_management_obj = CSVFileManagement(name_csv_str,"media/",'',',')
            CSV_file_management_obj.covert_to_header([
               "Truck Plan Ref.","PUS Record","Status",
               "Due Date","Release Time","Delivery Time",
               "Route Code","Trip","Truck License",
               "Driver Name"])
   
            truckplan_CSV_list = TruckplanPrintHelper.covert_data_list_to_CSV_list(truckplan_list)
            CSV_file_management_obj.covert_to_CSV_data_list(truckplan_CSV_list)
            return_name_CSV_str = CSV_file_management_obj.genearete_CSV_file()

            serializer_list =  TruckplanPrintHelper.covert_data_list_to_serializer_list(truckplan_list)

            serializer = serializerMapping.mapping_serializer_list(
                TruckPlan_list_Serializer_DTO,
                serializer_list,
                "success", 
                "",
                name_csv_str + '.csv',
                None,
                None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)


        except Exception as e:

            serializer = serializerMapping.mapping_serializer_list(
                    TruckPlan_list_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        

@api_view([ 'POST'])
def get_pickup_by_truckPlan_no(request):

    if request.method == 'POST':

        try:

            truckplan_data = JSONParser().parse(request)
            truckplan_obj = TruckPlan.objects.filter(truckplan_no= truckplan_data['truckPlan_no'])[0]

            pickUp_list = PickUp.objects.filter(
                due_date__year=truckplan_obj.due_date.year,
                due_date__month=truckplan_obj.due_date.month,
                due_date__day=truckplan_obj.due_date.day,
                route_code=truckplan_obj.route_code,
                route_trip=truckplan_obj.route_trip,
                status=2,
                is_active=True
            )

            pickUp_list = [pickUp for pickUp in pickUp_list if pickUp.truckplan_no == "" or pickUp.truckplan_no == truckplan_data['truckPlan_no']] 
        
            pickup_serializer_list =  PickUp_Serializer(pickUp_list,many=True)

            serializer = serializerMapping.mapping_serializer_list(
                PickUp_list_Serializer_DTO,
                pickup_serializer_list.data,
                "success", 
                "",
                None,
                None,
                None )

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:

            serializer = serializerMapping.mapping_serializer_list(
                    PickUp_list_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)

@api_view([ 'POST'])
def deleted_pickup_in_truckplan(request):

    if request.method == 'POST':

        try:

            pickup_data = JSONParser().parse(request)
            pickup_list = PickUp.objects.filter(pickup_no= pickup_data['pickup_no'])
            pickup_list.update(truckplan_no='')

            truckPlan_Serializer =  TruckPlan_Serializer(pickup_list,many=True)

            serializer = serializerMapping.mapping_serializer_list(
                TruckPlan_list_Serializer_DTO,
                truckPlan_Serializer.data,
                "success", 
                "",
                None,
                None,
                None )

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:

            serializer = serializerMapping.mapping_serializer_list(
                    TruckPlan_list_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        

@api_view([ 'POST'])
def add_pickup_in_truckplan(request):

    if request.method == 'POST':

        try:

            pickup_data = JSONParser().parse(request)
            pickup_list = PickUp.objects.filter(pickup_no= pickup_data['pickup_no'])

            pickup_list.update(truckplan_no=pickup_data['truckplan_no'])

            truckPlan_list = TruckPlan.objects.filter(truckplan_no=pickup_data['truckplan_no'])
            truckPlan_list.update(status=2)

            truckPlan_Serializer =  TruckPlan_Serializer(pickup_obj,many=True)

            serializer = serializerMapping.mapping_serializer_list(
                TruckPlan_list_Serializer_DTO,
                truckPlan_Serializer.data,
                "success", 
                "",
                None,
                None,
                None )

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:

            serializer = serializerMapping.mapping_serializer_list(
                    TruckPlan_list_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)

     

    

