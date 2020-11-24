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

        print('dsfsdfsdf')
        try:

            search_and_print_PUS_obj = JSONParser().parse(request)

            customer_code = search_and_print_PUS_obj['customer_code_selected']
            project_code = search_and_print_PUS_obj['project_code_selected']
            supplier_code = search_and_print_PUS_obj['supplier_code_selected']
            due_date_from = search_and_print_PUS_obj['due_date_from_selected']
            due_date_to = search_and_print_PUS_obj['due_date_to_selected']
            PUS_ref = search_and_print_PUS_obj['PUS_ref_selected']

            pickUp_serializer_list = truckPlanManagementService.search_pickUp_PUS(
                customer_code,
                project_code,
                supplier_code,
                due_date_from,
                due_date_to,
                PUS_ref
                )
 
            name_csv_str = "SearchAndPrintPUSCSV_" +datetime.now().strftime("%Y%m%d_%H%M%S")
            CSV_file_management_obj = CSVFileManagement(name_csv_str,"media/",'')

            header_list = ["PUS Ref","Status","Supplier","Plant","Order Count","Due Date","Release Time","Delivery Time","Route Code","Trip","Truck License","Driver Name"]
            CSV_file_management_obj.insert_header(header_list)
            csv_list = truckPlanManagementService.csv_list
            CSV_file_management_obj.covert_to_CSV_data_list(csv_list)
            return_name_CSV_str = CSV_file_management_obj.genearete_CSV_file()
      
            pickUp_list_serializer_DTO = serializerMapping.mapping_list_successful(
                pickUp_serializer_list,
                PickUp_list_Serializer_DTO,
                "",
                return_name_CSV_str)

            return JsonResponse(pickUp_list_serializer_DTO.data, status=status.HTTP_200_OK)

        except Exception as e:

            pickUp_list_serializer_error_DTO = serializerMapping.mapping_list_error(PickUp_list_Serializer_DTO,e)
            
            return JsonResponse(pickUp_list_serializer_error_DTO.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def generate_PUS(request):

    if request.method == 'POST':

        try:

            pickUp_list = JSONParser().parse(request)['orderList']

            pickUp_serializer = PickUp_Serializer(data=pickUp_list,many = True)

            if pickUp_serializer.is_valid():

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

            print(routerMaster_data)

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
     
            order_list_serializer_DTO = serializerMapping.mapping_list_successful(
                        order_serializer.data,
                        Order_list_Serializer_DTO,
                        "",
                        None)
            
            return JsonResponse(order_list_serializer_DTO.data, status=status.HTTP_200_OK)
        
        except Exception as e:

            order_serializer_error_DTO = serializerMapping.mapping_obj_error(Order_list_Serializer_DTO,e)

            return JsonResponse(order_serializer_error_DTO.data, status=status.HTTP_200_OK)


@api_view([ 'POST'])
def deleted_order_in_pickup(request):

    if request.method == 'POST':

        try:
            
            order_data = JSONParser().parse(request)
            print(order_data)
            order_obj = Order.objects.filter(order_no= order_data['order_no'])

            order_obj.update(pickup_no="")

            order_serializer =  OrderSerializer(order_obj)
     
            order_list_serializer_DTO = serializerMapping.mapping_list_successful(
                        order_serializer.data,
                        Order_list_Serializer_DTO,
                        "",
                        None)
            
            return JsonResponse(order_list_serializer_DTO.data, status=status.HTTP_200_OK)
        
        except Exception as e:

            order_serializer_error_DTO = serializerMapping.mapping_obj_error(Order_list_Serializer_DTO,e)

            return JsonResponse(order_serializer_error_DTO.data, status=status.HTTP_200_OK)


@api_view([ 'POST'])
def add_order_in_pickup(request):

    if request.method == 'POST':

        try:
            
            order_data = JSONParser().parse(request)
            order_obj = Order.objects.filter(order_no= order_data['order_no'])

            order_obj.update(pickup_no=order_data['pickup_no'])

            order_serializer =  OrderSerializer(order_obj)
     
            order_list_serializer_DTO = serializerMapping.mapping_list_successful(
                        order_serializer.data,
                        Order_list_Serializer_DTO,
                        "",
                        None)
            
            return JsonResponse(order_list_serializer_DTO.data, status=status.HTTP_200_OK)
       
            
            return JsonResponse(order_list_serializer_DTO.data, status=status.HTTP_200_OK)
        
        except Exception as e:

            order_serializer_error_DTO = serializerMapping.mapping_obj_error(Order_list_Serializer_DTO,e)

            return JsonResponse(order_serializer_error_DTO.data, status=status.HTTP_200_OK)


@api_view([ 'POST'])
def delete_pickUp(request):

    if request.method == 'POST':

        try:
            print("sadasdasd")
            pickUp_data = JSONParser().parse(request)

            pickUp_list = PickUp.objects.filter(pickup_no=pickUp_data['pickup_no'])
            pickUp_list.update(status=1)

            order_obj = Order.objects.filter(pickup_no=pickUp_data['pickup_no'])

            order_obj.update(pickup_no="")

            order_serializer =  OrderSerializer(order_obj)
     
            order_list_serializer_DTO = serializerMapping.mapping_list_successful(
                        order_serializer.data,
                        Order_list_Serializer_DTO,
                        "",
                        None)
            
            return JsonResponse(order_list_serializer_DTO.data, status=status.HTTP_200_OK)
       
            
            return JsonResponse(order_list_serializer_DTO.data, status=status.HTTP_200_OK)
        
        except Exception as e:

            order_serializer_error_DTO = serializerMapping.mapping_obj_error(Order_list_Serializer_DTO,e)

            return JsonResponse(order_serializer_error_DTO.data, status=status.HTTP_200_OK)


@api_view([ 'POST'])
def delete_truckplan(request):

    if request.method == 'POST':

        try:
   
            truckPlan_data = JSONParser().parse(request)

            truckPlan_list = TruckPlan.objects.filter(truckplan_no=truckPlan_data['truckplan_no'])
            truckPlan_list.update(status=1)

            pickUp_list = PickUp.objects.filter(truckplan_no=truckPlan_data['truckplan_no'])

            pickUp_list.update(truckplan_no="")

            pickUp_Serializer =  PickUp_Serializer(pickUp_list)
     
            pickUp_list_serializer_DTO = serializerMapping.mapping_list_successful(
                        pickUp_Serializer.data,
                        PickUp_list_Serializer_DTO,
                        "",
                        None)
            
            return JsonResponse(pickUp_list_serializer_DTO.data, status=status.HTTP_200_OK)
       
        except Exception as e:

            pickUp_serializer_error_DTO = serializerMapping.mapping_obj_error(PickUp_list_Serializer_DTO,e)

            return JsonResponse(pickUp_serializer_error_DTO.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def search_generate_truck_plan(request):

    if request.method == 'POST':

        try:

            search_generate_truck_plan_obj = JSONParser().parse(request)

            customer_code_selected_str = search_generate_truck_plan_obj['customer_code_selected']
            project_code_selected_str = search_generate_truck_plan_obj['project_code_selected']
            due_date_to_selected_str = search_generate_truck_plan_obj['due_date_to_selected']

            truckPlan_serializer_list = truckPlanManagementService.search_generate_truck_plan(
                customer_code_selected_str,
                project_code_selected_str,
                due_date_to_selected_str
                )
            
            name_csv_str = "SearchTruckPlanCSV_" +datetime.now().strftime("%Y%m%d_%H%M%S")
            CSV_file_management_obj = CSVFileManagement(name_csv_str,"media/",'')

            header_list = ["Truck Plan Ref.","Number of PUS","Due Date","Route Code","Trip"]
            CSV_file_management_obj.insert_header(header_list)
            csv_list = truckPlanManagementService.csv_list
            CSV_file_management_obj.covert_to_CSV_data_list(csv_list)
            return_name_CSV_str = CSV_file_management_obj.genearete_CSV_file()
      
            truckPlan_list_Serializer_DTO = serializerMapping.mapping_list_successful(
                truckPlan_serializer_list,
                TruckPlan_list_Serializer_DTO,
                "",
                return_name_CSV_str)

            return JsonResponse(truckPlan_list_Serializer_DTO.data, status=status.HTTP_200_OK)

        except Exception as e:

            truckPlan_list_serializer_error_DTO = serializerMapping.mapping_list_error(TruckPlan_list_Serializer_DTO,e)
            
            return JsonResponse(truckPlan_list_serializer_error_DTO.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def generate_truck_plan(request):

    if request.method == 'POST':

        try:

            truckPlant_list = JSONParser().parse(request)['orderPickList']
            print()
            truckPlant_added_list = []
     
            for truckPlant_obj in truckPlant_list :

                truckPlant_obj['due_date'] = datetime.strptime(truckPlant_obj['due_date'], "%d/%m/%Y").date()
                due_date_str = truckPlant_obj['due_date'].strftime("%Y%m%d") 


            truckPlan_Serializer = TruckPlan_Serializer(data=truckPlant_list,many = True)

            if truckPlan_Serializer.is_valid():

                truckPlan_Serializer.save(is_active=True,updated_by=request.user.username,updated_date=datetime.utcnow())

                truckPlan_serializer_DTO = serializerMapping.mapping_obj_successful(
                    truckPlan_Serializer.data,
                    TruckPlan_Serializer_DTO,
                    "",
                    None)

                return JsonResponse(truckPlan_serializer_DTO.data, status=status.HTTP_200_OK)
            
            truckPlan_serializer_error_DTO = serializerMapping.mapping_obj_error(TruckPlan_Serializer_DTO,truckPlan_Serializer.errors)

            return JsonResponse(truckPlan_serializer_error_DTO.data, status=status.HTTP_200_OK)
# 
        except Exception as e:

            truckPlan_serializer_error_DTO = serializerMapping.mapping_obj_error(TruckPlan_Serializer_DTO,e)
            
            return JsonResponse(truckPlan_serializer_error_DTO.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def search_and_print_truck_plan(request):

    if request.method == 'POST':

        try:

            print('makkuy')
            search_and_print_truck_plan_obj = JSONParser().parse(request)

            customer_code_selected_str = search_and_print_truck_plan_obj['customer_code_selected']
            project_code_selected_str = search_and_print_truck_plan_obj['project_code_selected']
            due_date_from_selected_str = search_and_print_truck_plan_obj['due_date_from_selected']
            due_date_to_selected_str = search_and_print_truck_plan_obj['due_date_to_selected']
            truck_plan_ref = search_and_print_truck_plan_obj['truck_plan_ref']

            truckPlan_serializer_list = truckPlanManagementService.search_and_print_truck_plan(
                customer_code_selected_str,
                project_code_selected_str,
                due_date_from_selected_str,
                due_date_to_selected_str,
                truck_plan_ref
                )
        
 
            name_csv_str = "SearchAndPrintTruckPlanCSV_" +datetime.now().strftime("%Y%m%d_%H%M%S")
            CSV_file_management_obj = CSVFileManagement(name_csv_str,"media/",'')

            header_list = ["Truck Plan Ref.","PUS Record","Status","Due Date","Release Time","Delivery Time","Route Code","Trip","Truck License","Driver Name"]
            CSV_file_management_obj.insert_header(header_list)
            csv_list = truckPlanManagementService.csv_list
            CSV_file_management_obj.covert_to_CSV_data_list(csv_list)
            return_name_CSV_str = CSV_file_management_obj.genearete_CSV_file()
      
            truckPlan_list_serializer_DTO = serializerMapping.mapping_list_successful(
                truckPlan_serializer_list,
                TruckPlan_list_Serializer_DTO,
                "",
                return_name_CSV_str)

            return JsonResponse(truckPlan_list_serializer_DTO.data, status=status.HTTP_200_OK)

        except Exception as e:

            truckPlan_list_serializer_error_DTO = serializerMapping.mapping_list_error(TruckPlan_list_Serializer_DTO,e)
            
            return JsonResponse(truckPlan_list_serializer_error_DTO.data, status=status.HTTP_200_OK)


@api_view([ 'POST'])
def get_pickup_by_truckPlan_no(request):

    if request.method == 'POST':

        try:

            truckPlan_data = JSONParser().parse(request)
            truckPlan_obj = TruckPlan.objects.filter(truckplan_no= truckPlan_data['truckPlan_no'])[0]

            pickUp_list = PickUp.objects.filter(
                            due_date__year=truckPlan_obj.due_date.year,
                            due_date__month=truckPlan_obj.due_date.month,
                            due_date__day=truckPlan_obj.due_date.day,
                            route_code=truckPlan_obj.route_code,
                            route_trip=truckPlan_obj.route_trip,
                            status=2,
                            is_active=True
                            )
            pickUp_list = [pickUp for pickUp in pickUp_list if pickUp.truckplan_no == "" or pickUp.truckplan_no == truckPlan_data['truckPlan_no']] 

            pickUp_serializer =  PickUp_Serializer(pickUp_list,many=True)
     
            pickUp_list_serializer_DTO = serializerMapping.mapping_list_successful(
                        pickUp_serializer.data,
                        PickUp_list_Serializer_DTO,
                        "",
                        None)
            
            return JsonResponse(pickUp_list_serializer_DTO.data, status=status.HTTP_200_OK)
        
        except Exception as e:

            pickUp_serializer_error_DTO = serializerMapping.mapping_obj_error(PickUp_list_Serializer_DTO,e)

            return JsonResponse(pickUp_serializer_error_DTO.data, status=status.HTTP_200_OK)

@api_view([ 'POST'])
def deleted_pickup_in_truckplan(request):

    if request.method == 'POST':

        try:
            
            pickup_data = JSONParser().parse(request)
            pickup_obj = PickUp.objects.filter(pickup_no= pickup_data['pickup_no'])
            pickup_obj.update(truckplan_no='')

            truckPlan_Serializer =  TruckPlan_Serializer(pickup_obj)
     
            truckPlan_list_serializer_DTO = serializerMapping.mapping_list_successful(
                        truckPlan_Serializer.data,
                        TruckPlan_Serializer_DTO,
                        "",
                        None)
            
            return JsonResponse(truckPlan_list_serializer_DTO.data, status=status.HTTP_200_OK)
       
        
        except Exception as e:

            truckPlan_list_Serializer_DTO = serializerMapping.mapping_obj_error(TruckPlan_list_Serializer_DTO,e)

            return JsonResponse(truckPlan_list_Serializer_DTO.data, status=status.HTTP_200_OK)

@api_view([ 'POST'])
def add_pickup_in_truckplan(request):

    if request.method == 'POST':

        try:
            
            pickup_data = JSONParser().parse(request)
            pickup_obj = PickUp.objects.filter(pickup_no= pickup_data['pickup_no'])

            pickup_obj.update(truckplan_no=pickup_data['truckplan_no'])


            truckPlan_Serializer =  TruckPlan_Serializer(pickup_obj)
     
            truckPlan_list_serializer_DTO = serializerMapping.mapping_obj_successful(
                        truckPlan_Serializer.data,
                        TruckPlan_Serializer_DTO,
                        "",
                        None)
            
            return JsonResponse(truckPlan_list_serializer_DTO.data, status=status.HTTP_200_OK)
        
        except Exception as e:

            truckPlan_serializer_error_DTO = serializerMapping.mapping_obj_error(TruckPlan_Serializer_DTO,e)

            return JsonResponse(truckPlan_serializer_error_DTO.data, status=status.HTTP_200_OK)

    

