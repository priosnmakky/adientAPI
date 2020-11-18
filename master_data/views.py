from django.shortcuts import render
from django.http.response import JsonResponse

from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from datetime import datetime
from master_data.models import Part,RouterMaster,Project,Customer,Package,Station,Truck,Driver,RouterInfo,CalendarMaster
from master_data.serializers import Part_Serializer,Part_Serializer_DTO,Part_list_Serializer_DTO
from master_data.serializers import Project_Serializer,Project_Serializer_DTO,Project_list_Serializer_DTO
from master_data.serializers import Customer_Serializer,Customer_Serializer_DTO,Customer_list_Serializer_DTO
from master_data.serializers import Package_Serializer,Package_Serializer_DTO,Package_list_Serializer_DTO
from master_data.serializers import Station_Serializer,Station_list_Serializer_DTO
from master_data.serializers import Plant_Serializer,Plant_list_Serializer_DTO
from master_data.serializers import Truck_Serializer,Truck_Serializer_DTO,Truck_list_Serializer_DTO
from master_data.serializers import Driver_Serializer,Driver_Serializer_DTO,Driver_list_Serializer_DTO
from master_data.serializers import RouterInfo_Serializer,RouterInfo_Serializer_DTO,RouterInfo_list_Serializer_DTO
from master_data.serializers import CalendarMaster_Serializer,CalendarMaster_Serializer_DTO,CalendarMaster_list_Serializer_DTO
from master_data.serializers import RouterMaster_Serializer,RouterMaster_Serializer_DTO,RouterMaster_list_Serializer_DTO
from master_data.serializers import File_Serializer,validate_error_serializer,validate_warning_serializer
from model_DTO.base_DTO import base_DTO
from model_DTO.marter_data.Customer_DTO import Customer_DTO
from master_data.model_dto.RouteMasterDTO import RouteMasterDTO
from master_data.model_dto.RouteInfoDTO import RouteInfoDTO
from rest_framework.permissions import IsAuthenticated
import csv
import uuid
from django.core.files.storage import FileSystemStorage
from model_DTO.validateError import validateError,validateErrorList
import re
import pandas as pd
from decimal import Decimal
from app.helper.config.ConfigMessage import ConfigMessage
from app.helper.error_helper.ErrorHelper import ErrorHelper
from app.serializersMapping.SerializerMapping import SerializerMapping
from rest_framework.response import Response
from app.services.project_service.ProjectService import ProjectService
from app.helper.project_helper.ProjectHelper import ProjectHepler
from app.services.customer_service.CustomerService import CustomerService
from app.helper.customer_helper.CustomerHelper import CustomerHelper
from app.helper.CSV_file_management.CSVFileManagement import CSVFileManagement
from app.services.calendarMaster_service.CalendarMasterService import CalendarMasterService
from app.helper.calendarMaster_helper.CalendarMasterHelper import CalendarMasterHelper
from app.helper.file_management.FileManagement import FileManagement
from app.helper.package_helper.PackageHelper import PackageHelper
from app.services.package_service.PackageService import PackageService
from app.helper.part_helper.PartHelper import PartHelper
from app.services.part_service.PartService import PartService
import json


configMessage = ConfigMessage()
serializerMapping = SerializerMapping()


@api_view(['GET', 'POST', 'DELETE'])
def part_list(request):
    
    if request.method == 'GET':
        try:
            part_list = Part.objects.filter(is_active = True)

            serializer = serializerMapping.mapping_serializer_list(
                Part_list_Serializer_DTO,
                part_list,
                "success", 
                "",
                "",
                None,
                None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:

            serializer = serializerMapping.mapping_serializer_list(
                    Part_list_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None )

            return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':


        try:

            part_data = JSONParser().parse(request)
            part_serializer_obj = Part_Serializer(data=part_data)
    
            if part_serializer_obj.is_valid():

                part_serializer_obj.save()
                part_obj =  part_serializer_obj.save(updated_by=request.user.username)

                serializer = serializerMapping.mapping_serializer_obj(
                Part_Serializer_DTO,
                part_obj,
                "success", 
                configMessage.configs.get("PART_MASTER_ADD_MASSAGE_SUCCESSFUL").data,
                "",
                None,
                None )
            
            else : 
                
                serializer = serializerMapping.mapping_serializer_obj(
                    Part_Serializer_DTO,
                    None,
                    "Error",
                    ErrorHelper.get_error_massage(part_serializer_obj.errors),
                    None,
                    None,
                    None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:

            serializer = serializerMapping.mapping_serializer_obj(
                Part_Serializer_DTO,
                None,
                "Error",
                e,
                None,
                None,
                None )
                
            return Response(serializer.data, status=status.HTTP_200_OK)
         

@api_view(['GET', 'POST', 'DELETE'])
def comfirm_part(request):   
     if request.method == 'POST':
        try: 
            part_data = JSONParser().parse(request)
        
            for part_obj in part_data:

                add_part_obj = Part.objects.filter( part_number = part_obj["part_number"] )
                part_obj['status'] = 2
                part_serializer_obj = Part_Serializer(add_part_obj[0],data=part_obj)

                if part_serializer_obj.is_valid():

                    part_serializer_obj.save()
            
            serializer = serializerMapping.mapping_serializer_list(
                Part_list_Serializer_DTO,
                None,
                "success", 
                "",
                "",
                None,
                None )

            return Response(serializer.data, status=status.HTTP_200_OK)

                

        except Exception as e:

            serializer = serializerMapping.mapping_serializer_list(
                    Part_list_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None )

            return Response(serializer.data, status=status.HTTP_200_OK)
   

@api_view(['GET', 'POST', 'DELETE'])
def edited_part(request):

    if request.method == 'POST':

        try:

            part_data = JSONParser().parse(request)
            part_obj = Part.objects.filter( part_number = part_data["part_number"] )[0]
            part_serializer_obj = Part_Serializer(part_obj,data=part_data)

            if part_serializer_obj.is_valid():

                part_serializer_obj.save()

                serializer = serializerMapping.mapping_serializer_obj(
                    Part_Serializer_DTO,
                    part_obj,
                    "success", 
                    configMessage.configs.get("PART_MASTER_EDIT_MASSAGE_SUCCESSFUL").data,
                    "",
                    None,
                    None 
                    )
            
            else :

                serializer = serializerMapping.mapping_serializer_obj(
                    Part_Serializer_DTO,
                    None,
                    "Error",
                    ErrorHelper.get_error_massage(part_serializer_obj.errors),
                    None,
                    None,
                    None )
                    
            
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:

            serializer = serializerMapping.mapping_serializer_obj(
                    Part_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def search_part(request):

    if request.method == 'POST':

        try:

            part_data_obj = JSONParser().parse(request)

            customer_code = part_data_obj['customer_selected']
            project_code = part_data_obj['project_selected']
            supplier_code = part_data_obj['supplier_selected']
            status = part_data_obj['status_selected']
            part_number = part_data_obj['partNumber_selected']

            partService  = PartService()
            part_list =  partService.search_part(customer_code,project_code,supplier_code,status,part_number)

            name_csv_str = "PartMasterCSV_" +datetime.now().strftime("%Y%m%d_%H%M%S")
            CSV_file_management_obj = CSVFileManagement(name_csv_str,"media/",'',',')
            CSV_file_management_obj.covert_to_header([
                "Project Code",
                "status",
                "Supplier Code",
                "Part Number",
                "Part Name",
                "Package No",
                "Package Volume",
                "Part Weight",
                "Remark",
                "Update By",
                "Update Date",])

            part_CSV_list = PartHelper.covert_data_list_to_CSV_list(part_list)
            CSV_file_management_obj.covert_to_CSV_data_list(part_CSV_list)
            return_name_CSV_str = CSV_file_management_obj.genearete_CSV_file()

            serializer_list =  PartHelper.covert_data_list_to_serializer_list(part_list)

            serializer = serializerMapping.mapping_serializer_list(
                    Part_list_Serializer_DTO,
                    serializer_list,
                    "success", 
                    "",
                    name_csv_str + '.csv',
                    None,
                    None
                )


            return JsonResponse(serializer.data, safe=False)
        
        except Exception as e:

            serializer = serializerMapping.mapping_serializer_list(
                    Part_list_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None 
                )
            
            return JsonResponse(serializer.data, safe=False)
            
            

@api_view(['GET', 'POST', 'DELETE'])
def deleted_part(request):

    if request.method == 'POST':

        try:

            part_data = JSONParser().parse(request)
            part_list = Part.objects.filter(part_number__in=part_data)
            part_list.update(is_active = False)

            serializer = serializerMapping.mapping_serializer_list(
                Part_list_Serializer_DTO,
                part_list,
                "success", 
                configMessage.configs.get("STATION_MASTER_DELETE_MASSAGE_SUCCESSFUL").data,
                "",
                None,
                None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:

            serializer = serializerMapping.mapping_serializer_list(
                    Part_list_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST', 'DELETE'])
def router_list(request):
    
    if request.method == 'GET':
        try:
            router_list = RouterMaster.objects.filter(is_active=True)
            router_serializer = Router_master_Serializer(router_list, many=True)

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "success"
            base_DTO_obj.massage = "get router"
            base_DTO_obj.data_list = router_serializer.data

            router_list_Serializer_DTO_obj = Router_master_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(router_list_Serializer_DTO_obj.data, status=status.HTTP_200_OK)
        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "error"
            base_DTO_obj.massage = "error"
            # base_DTO_obj.data_list = order_serializer.data

            router_list_Serializer_DTO_obj = Router_master_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(router_list_Serializer_DTO_obj.data, status=status.HTTP_200_OK)

        

            # return JsonResponse(order_serializer.data, safe=False)

    elif request.method == 'POST':


        try:
            router_data = JSONParser().parse(request)
            router_serializer_obj = Router_master_Serializer(data=router_data)
            

            if router_serializer_obj.is_valid():

                router_serializer_obj.save()

                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "success"
                base_DTO_obj.massage = "save part is successful"
                base_DTO_obj.data = router_serializer_obj.data

                router_Serializer_DTO_reponse = Router_master_Serializer_DTO(base_DTO_obj)

                return JsonResponse(router_Serializer_DTO_reponse.data, status=status.HTTP_200_OK) 
            
            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = router_serializer_obj.errors
            base_DTO_obj.data = router_serializer_obj.data

            router_Serializer_DTO_reponse = Router_master_Serializer_DTO(base_DTO_obj)

            return JsonResponse(router_Serializer_DTO_reponse.data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = e
            base_DTO_obj.data = None

            router_Serializer_DTO_reponse = Router_master_Serializer_DTO(base_DTO_obj)

        return JsonResponse(router_Serializer_DTO_reponse.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST', 'DELETE'])
def supplier_list(request):
    
    if request.method == 'GET':
        try:
            station_list = Station.objects.filter(station_type = 'SUPPLIER',is_active=True)
            station_serializer = Station_Serializer(station_list, many=True)

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "success"
            base_DTO_obj.massage = "get router"
            base_DTO_obj.data_list = station_serializer.data

            station_list_Serializer_DTO_obj = Station_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(station_list_Serializer_DTO_obj.data, status=status.HTTP_200_OK)
        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "error"
            base_DTO_obj.massage = e
            # base_DTO_obj.data_list = order_serializer.data

            station_list_Serializer_DTO_obj = Station_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(station_list_Serializer_DTO_obj.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'DELETE'])
def plant_list(request):
    

    if request.method == 'GET':
        try:
            station_list = Station.objects.filter(station_type = 'PLANT',is_active=True)
            station_serializer = Station_Serializer(station_list, many=True)

            print(station_list)

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "success"
            base_DTO_obj.massage = "get router"
            base_DTO_obj.data_list = station_serializer.data

            station_list_Serializer_DTO_obj = Station_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(station_list_Serializer_DTO_obj.data, status=status.HTTP_200_OK)
        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "error"
            base_DTO_obj.massage = "error"
            # base_DTO_obj.data_list = order_serializer.data

            station_list_Serializer_DTO_obj = Station_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(station_list_Serializer_DTO_obj.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'DELETE'])
def project_list(request):

    if request.method == 'GET':

        try : 

            project_list = Project.objects.filter(is_active=True)

            serializer = serializerMapping.mapping_serializer_list(
                Project_list_Serializer_DTO,
                project_list,
                "success", 
                "",
                "",
                None,
                None )


            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:

            serializer = serializerMapping.mapping_serializer_list(
                    Project_list_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':

        try:

            project_data = JSONParser().parse(request)

            project_serializer_obj = Project_Serializer(data=project_data)

            if project_serializer_obj.is_valid():

                project_serializer_obj.save()
                project_list =  project_serializer_obj.save(updated_by=request.user.username)

         
                serializer = serializerMapping.mapping_serializer_obj(
                Project_list_Serializer_DTO,
                project_list,
                "success", 
                configMessage.configs.get("PROJECT_MASTER_ADD_MASSAGE_SUCCESSFUL").data,
                "",
                None,
                None )
            
            else : 
                
                serializer = serializerMapping.mapping_serializer_obj(
                    Project_list_Serializer_DTO,
                    None,
                    "Error",
                    ErrorHelper.get_error_massage(project_serializer_obj.errors),
                    None,
                    None,
                    None )
                    
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:

            serializer = serializerMapping.mapping_serializer_obj(
                    Project_list_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST', 'DELETE'])
def deleted_project(request):

    if request.method == 'POST':

        try:

            project_data = JSONParser().parse(request)

            project_list = Project.objects.filter(project_code__in=project_data)
            project_list.update(is_active = False)

            serializer = serializerMapping.mapping_serializer_list(
                Project_list_Serializer_DTO,
                project_list,
                "success", 
                configMessage.configs.get("PROJECT_MASTER_DELETE_MASSAGE_SUCCESSFUL").data,
                "",
                None,
                None )

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:

            serializer = serializerMapping.mapping_serializer_list(
                    Project_list_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST', 'DELETE'])
def edited_project(request):

    if request.method == 'POST':

        try:

            project_data = JSONParser().parse(request)
            project_obj = Project.objects.filter( project_code = project_data["project_code"] )
            project_serializer_obj = Project_Serializer(project_obj[0],data=project_data)


            if project_serializer_obj.is_valid():
                
                project_serializer_obj.save()


                serializer = serializerMapping.mapping_serializer_obj(
                Project_Serializer_DTO,
                project_obj,
                "success", 
                "",
                "",
                None,
                None )
            
            else : 

                serializer = serializerMapping.mapping_serializer_obj(
                    Project_Serializer_DTO,
                    None,
                    "Error",
                    ErrorHelper.get_error_massage(project_serializer_obj.errors),
                    None,
                    None,
                    None )
                    
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:

            serializer = serializerMapping.mapping_serializer_list(
                    Project_list_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def search_project(request):

    if request.method == 'POST':

        try:

           
            project_data_obj = JSONParser().parse(request)
            customer_code = project_data_obj['customer_code']

            projectService = ProjectService()
            project_list =  projectService.search_project(customer_code)
            
            name_csv_str = "ProjectMasterCSV" +datetime.now().strftime("%Y%m%d_%H%M%S")
            CSV_file_management_obj = CSVFileManagement(name_csv_str,"media/",'',',')
            CSV_file_management_obj.covert_to_header([
               "Project Code",
                "Customer Code",
                "Remark",
                "Updated By",
                "Updated Date",])
            project_CSV_list = ProjectHepler.covert_data_list_to_CSV_list(project_list)
            CSV_file_management_obj.covert_to_CSV_data_list(project_CSV_list)
            return_name_CSV_str = CSV_file_management_obj.genearete_CSV_file()

            serializer_list =  ProjectHepler.covert_data_list_to_serializer_list(project_list)

            serializer = serializerMapping.mapping_serializer_list(
                Project_list_Serializer_DTO,
                serializer_list,
                "success", 
                "",
                name_csv_str + '.csv',
                None,
                None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:

            serializer = serializerMapping.mapping_serializer_list(
                    Project_list_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'DELETE'])
def customer_list(request):
    
    if request.method == 'GET':
        try:
            customer_list = Customer.objects.all()
        
            serializer = serializerMapping.mapping_serializer_list(
                Customer_list_Serializer_DTO,
                customer_list,
                "success", 
                "",
                "",
                None,
                None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:

            serializer = serializerMapping.mapping_serializer_list(
                    Customer_list_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None )

            return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':

        try:

            customer_data = JSONParser().parse(request)
            customer_serializer_obj = Customer_Serializer(data=customer_data)

            if customer_serializer_obj.is_valid():

                customer_serializer_obj.save()
                customer_obj =  customer_serializer_obj.save(updated_by=request.user.username)

                serializer = serializerMapping.mapping_serializer_obj(
                Customer_Serializer_DTO,
                customer_obj,
                "success", 
                configMessage.configs.get("STATION_MASTER_ADD_MASSAGE_SUCCESSFUL").data,
                "",
                None,
                None )
            
            else : 
                
                serializer = serializerMapping.mapping_serializer_obj(
                    Customer_Serializer_DTO,
                    None,
                    "Error",
                    ErrorHelper.get_error_massage(customer_serializer_obj.errors),
                    None,
                    None,
                    None )
                    
            
            return Response(serializer.data, status=status.HTTP_200_OK)


        except Exception as e:

            serializer = serializerMapping.mapping_serializer_obj(
                Customer_Serializer_DTO,
                None,
                "Error",
                e,
                None,
                None,
                None )
                
            return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['GET', 'POST', 'DELETE'])
def deleted_customer(request):

    if request.method == 'POST':

        try:

            station_data = JSONParser().parse(request)
            station_list = Station.objects.filter(station_code__in=station_data)
            station_list.update(is_active = False)

            calendarMaster_list = CalendarMaster.objects.filter(plant_code__in=station_data)
            calendarMaster_list.update(is_active = False)

            serializer = serializerMapping.mapping_serializer_list(
                Customer_list_Serializer_DTO,
                station_list,
                "success", 
                configMessage.configs.get("STATION_MASTER_DELETE_MASSAGE_SUCCESSFUL").data,
                "",
                None,
                None )

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:

            serializer = serializerMapping.mapping_serializer_list(
                    Customer_list_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'DELETE'])
def edited_customer(request):

    if request.method == 'POST':

        try:

            customer_data = JSONParser().parse(request)

            station_list = Station.objects.filter( station_code = customer_data["station_code"] )
            customer_serializer_obj = Customer_Serializer(station_list[0],data=customer_data)

            if customer_serializer_obj.is_valid():
                
                customer_serializer_obj.save()

                serializer = serializerMapping.mapping_serializer_list(
                Customer_list_Serializer_DTO,
                station_list,
                "success", 
                configMessage.configs.get("STATION_MASTER_EDIT_MASSAGE_SUCCESSFUL").data,
                "",
                None,
                None )
            
            else : 

                serializer = serializerMapping.mapping_serializer_list(
                    Customer_list_Serializer_DTO,
                    None,
                    "Error",
                    ErrorHelper.get_error_massage(customer_serializer_obj.errors),
                    None,
                    None,
                    None )
                    
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:

            serializer = serializerMapping.mapping_serializer_list(
                    Customer_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['POST'])
def search_customer(request):

    if request.method == 'POST':

        try:

            customer_data_obj = JSONParser().parse(request)
            project_code = customer_data_obj['project_code']
            customer_code = customer_data_obj['customer_code']
            stationCode_code = customer_data_obj['stationCode_selected']

            customerService = CustomerService()
            customer_list =  customerService.search_customer(customer_code,project_code,stationCode_code)

            name_csv_str = "StationMasterCSV" +datetime.now().strftime("%Y%m%d_%H%M%S")
            CSV_file_management_obj = CSVFileManagement(name_csv_str,"media/",'',',')
            CSV_file_management_obj.covert_to_header([
               "Customer",
                "Project",
                "Station Code",
                "Descrition",
                "type",
                "Zone",
                "Province",
                "Address",
                "Remark",
                "Update By",
                "Update Date"])
            customer_CSV_list = CustomerHelper.covert_data_list_to_CSV_list(customer_list)
            CSV_file_management_obj.covert_to_CSV_data_list(customer_CSV_list)
            return_name_CSV_str = CSV_file_management_obj.genearete_CSV_file()

            serializer_list =  CustomerHelper.covert_data_list_to_serializer_list(customer_list)

        
            serializer = serializerMapping.mapping_serializer_list(
                Customer_list_Serializer_DTO,
                serializer_list,
                "success", 
                "",
                name_csv_str + '.csv',
                None,
                None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:

            serializer = serializerMapping.mapping_serializer_list(
                    Customer_list_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'DELETE'])
def package_list(request):
    
    if request.method == 'GET':
        try:

            package_list = Package.objects.filter(is_active=True)

            serializer = serializerMapping.mapping_serializer_list(
                Package_list_Serializer_DTO,
                package_list,
                "success", 
                "",
                "",
                None,
                None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:

            serializer = serializerMapping.mapping_serializer_list(
                    Package_list_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None )

            return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':

        try:
            

            packageHelper = PackageHelper()

            packages_data = json.loads(request.POST['packages'])

            package_create_obj = packageHelper.create(packages_data)

            if package_create_obj == None :

                serializer = serializerMapping.mapping_serializer_obj(
                    Package_Serializer_DTO,
                    None,
                    "Error",
                    packageHelper.massage_error,
                    None,
                    None,
                    None )
            
            else : 

                image_url = ''
                try: 

                    fileManagement = FileManagement('media/')
                    image_url = fileManagement.save_file(package_create_obj.package_no+".png",request.FILES['file'])
                    packages_data['image_url'] = image_url
                    packageHelper.update(packages_data)

                except:

                    print('err')

                package_serializer = Package_Serializer(data={'packages' : request.POST['packages']})

            
                serializer = serializerMapping.mapping_serializer_obj(
                Package_Serializer_DTO,
                package_serializer,
                "success", 
                configMessage.configs.get("PACKAGES_MASTER_ADD_MASSAGE_SUCCESSFUL").data,
                "",
                None,
                None )

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:

            serializer = serializerMapping.mapping_serializer_obj(
                Package_Serializer_DTO,
                None,
                "Error",
                e,
                None,
                None,
                None )
                
            return Response(serializer.data, status=status.HTTP_200_OK)

     

@api_view(['GET', 'POST', 'DELETE'])
def deleted_package(request):

     if request.method == 'POST':
        
        try:

            package_data = JSONParser().parse(request)
            package_list = Package.objects.filter(package_no__in=package_data)
            package_list.update(is_active = False)


            serializer = serializerMapping.mapping_serializer_list(
                Package_list_Serializer_DTO,
                package_list,
                "success", 
                configMessage.configs.get("PACKAGES_MASTER_DELETE_MASSAGE_SUCCESSFUL").data,
                "",
                None,
                None )

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:

            serializer = serializerMapping.mapping_serializer_list(
                    Package_list_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)

      
@api_view(['GET', 'POST', 'DELETE'])
def edited_package(request):

    if request.method == 'POST':

        try:

            packageHelper = PackageHelper()
            package_data = json.loads(request.POST['packages'])

            package_update_obj = packageHelper.update(package_data)

            if package_update_obj == None :

                serializer = serializerMapping.mapping_serializer_obj(
                    Package_Serializer_DTO,
                    None,
                    "Error",
                    packageHelper.massage_error,
                    None,
                    None,
                    None )
            
            else : 

                image_url = ''
                try: 
                    image_name_str = "image_" +datetime.now().strftime("%Y%m%d_%H%M%S")+".png"
                    fileManagement = FileManagement('media/')
                    image_url = fileManagement.save_file(image_name_str,request.FILES['file'])
                    package_data['image_url'] = image_url
                    packageHelper.update(package_data)

                except:

                    print('err')

                package_serializer = Package_Serializer(data={'packages' : request.POST['packages']})

                serializer = serializerMapping.mapping_serializer_obj(
                Package_Serializer_DTO,
                package_serializer,
                "success", 
                configMessage.configs.get("PACKAGES_MASTER_EDIT_MASSAGE_SUCCESSFUL").data,
                "",
                None,
                None )

            return Response(serializer.data, status=status.HTTP_200_OK)
               

        except Exception as e:

            serializer = serializerMapping.mapping_serializer_obj(
                Package_Serializer_DTO,
                None,
                "Error",
                e,
                None,
                None,
                None )
                
            return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def search_package(request):

    if request.method == 'POST':

        try:

            package_data_obj = JSONParser().parse(request)

            customer_code = package_data_obj['customer_selected']
            project_code = package_data_obj['project_selected']
            supplier_code = package_data_obj['supplier_selected']
            package_code = package_data_obj['packageCode_selected']
            package_no = package_data_obj['packageNo_selected']

            packageService = PackageService()
            package_list = packageService.search_package(customer_code,project_code,supplier_code,package_code,package_no)
     
            name_csv_str = "PackageMasterCSV_" +datetime.now().strftime("%Y%m%d_%H%M%S")
            CSV_file_management_obj = CSVFileManagement(name_csv_str,"media/",'',',')
            CSV_file_management_obj.covert_to_header([
               "Supplier Code",
                "Package Code",
                "Package No",
                "SNP",
                "W (mm.)",
                "L (mm.)",
                "H (mm.)",
                "Weight (Kg)",
                "Is There Image",
                "Update By",
                "Update Date",])
            package_CSV_list = PackageHelper.covert_data_list_to_CSV_list(package_list)
            CSV_file_management_obj.covert_to_CSV_data_list(package_CSV_list)
            return_name_CSV_str = CSV_file_management_obj.genearete_CSV_file()

            serializer_list =  PackageHelper.covert_data_list_to_serializer_list(package_list)

            serializer = serializerMapping.mapping_serializer_list(
                Package_list_Serializer_DTO,
                serializer_list,
                "success", 
                "",
                name_csv_str + '.csv',
                None,
                None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:

            serializer = serializerMapping.mapping_serializer_list(
                    Package_list_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)

  

@api_view(['GET', 'POST', 'DELETE'])
def truck_list(request):
    
    if request.method == 'GET':
        try:
            truck_list = Truck.objects.filter(is_active=True)
            truck_serializer_obj = Truck_Serializer(truck_list, many=True)

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "success"
            base_DTO_obj.massage = "get truck"
            base_DTO_obj.data_list = truck_serializer_obj.data

            truck_list_Serializer_DTO_obj = Truck_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(truck_list_Serializer_DTO_obj.data, status=status.HTTP_200_OK)
        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "error"
            base_DTO_obj.massage = e 
            # base_DTO_obj.data_list = order_serializer.data

            truck_list_Serializer_DTO_obj = Truck_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(truck_list_Serializer_DTO_obj.data, status=status.HTTP_200_OK)

        

            # return JsonResponse(order_serializer.data, safe=False)

    elif request.method == 'POST':


        try:
            truck_data = JSONParser().parse(request)

            if truck_data['truck_license'] is None or truck_data['truck_license'].strip() == "" :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("TRUCK_MASTER_TRUCKLICENSE_REQUIRED").data
                base_DTO_obj.data = None

                truck_Serializer_DTO = Truck_Serializer_DTO(base_DTO_obj)

                return JsonResponse(truck_Serializer_DTO.data, status=status.HTTP_200_OK) 
            
            elif truck_data['province'] is None or truck_data['province'].strip() == "" :

                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("TRUCK_MASTER_PROVINCE_REQUIRED").data
                base_DTO_obj.data = None

                truck_Serializer_DTO = Truck_Serializer_DTO(base_DTO_obj)

                return JsonResponse(truck_Serializer_DTO.data, status=status.HTTP_200_OK) 
            
            elif truck_data['truck_type'] is None or truck_data['truck_type'].strip() == "" :

                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("TRUCK_MASTER_TRUCKTYPE_REQUIRED").data
                base_DTO_obj.data = None

                truck_Serializer_DTO = Truck_Serializer_DTO(base_DTO_obj)

                return JsonResponse(truck_Serializer_DTO.data, status=status.HTTP_200_OK) 
            
            
            elif truck_data['fuel_type'] is None or truck_data['fuel_type'].strip() == "" :

                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("TRUCK_MASTER_FUELTYPE_REQUIRED").data
                base_DTO_obj.data = None

                truck_Serializer_DTO = Truck_Serializer_DTO(base_DTO_obj)

                return JsonResponse(truck_Serializer_DTO.data, status=status.HTTP_200_OK)
            
            elif truck_data['max_speed'] is None or truck_data['max_speed'] == "" :

                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("TRUCK_MASTER_MAXSPEED_REQUIRED").data
                base_DTO_obj.data = None

                truck_Serializer_DTO = Truck_Serializer_DTO(base_DTO_obj)

                return JsonResponse(truck_Serializer_DTO.data, status=status.HTTP_200_OK)
            
            elif truck_data['max_volume'] is None or truck_data['max_volume'] == "" :

                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("TRUCK_MASTER_MAXVOLUME_REQUIRED").data
                base_DTO_obj.data = None

                truck_Serializer_DTO = Truck_Serializer_DTO(base_DTO_obj)

                return JsonResponse(truck_Serializer_DTO.data, status=status.HTTP_200_OK)
            
            elif truck_data['max_weight'] is None or truck_data['max_weight'] == "" :

                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("TRUCK_MASTER_MAXWEIGHT_REQUIRED").data
                base_DTO_obj.data = None

                truck_Serializer_DTO = Truck_Serializer_DTO(base_DTO_obj)

                return JsonResponse(truck_Serializer_DTO.data, status=status.HTTP_200_OK)
            
            else : 

                truck_list = Truck.objects.filter(truck_license = truck_data['truck_license'])
            
         
                if len(truck_list) >0 :

                    if truck_list[0].is_active :

                        base_DTO_obj =  base_DTO()
                        base_DTO_obj.serviceStatus = "Error"
                        base_DTO_obj.massage = configMessage.configs.get("TRUCK_MASTER_DUPLICATE").data
                        base_DTO_obj.data = None

                        truck_Serializer_DTO_reponse = Truck_Serializer_DTO(base_DTO_obj)

                        return JsonResponse(truck_Serializer_DTO_reponse.data, status=status.HTTP_200_OK) 
                    
                    else:

                        truck_list.update(
                            province=truck_data['province'],
                            truck_type=truck_data['truck_type'],
                            fuel_type=truck_data['fuel_type'],
                            max_speed=Decimal(truck_data['max_speed']),
                            max_volume=Decimal(truck_data['max_volume']),
                            max_weight=Decimal(truck_data['max_weight']),
                            is_active = True
                        )

                        base_DTO_obj =  base_DTO()
                        base_DTO_obj.serviceStatus = "success"
                        base_DTO_obj.massage = configMessage.configs.get("TRUCK_MASTER_ADD_MASSAGE_SUCCESSFUL").data
                        base_DTO_obj.data = None

                        truck_Serializer_DTO_reponse = Truck_Serializer_DTO(base_DTO_obj)

                        return JsonResponse(truck_Serializer_DTO_reponse.data, status=status.HTTP_200_OK)

                truck_serializer_obj = Truck_Serializer(data=truck_data)
            
                if truck_serializer_obj.is_valid():

                    truck_serializer_obj.save()

                    base_DTO_obj =  base_DTO()
                    base_DTO_obj.serviceStatus = "success"
                    base_DTO_obj.massage = configMessage.configs.get("TRUCK_MASTER_ADD_MASSAGE_SUCCESSFUL").data
                    base_DTO_obj.data = truck_serializer_obj.data

                    truck_Serializer_DTO_reponse = Truck_Serializer_DTO(base_DTO_obj)

                    return JsonResponse(truck_Serializer_DTO_reponse.data, status=status.HTTP_200_OK) 
                
                else :
                
                    base_DTO_obj =  base_DTO()
                    base_DTO_obj.serviceStatus = "Error"
                    base_DTO_obj.massage = truck_serializer_obj.errors
                    base_DTO_obj.data = None

                    truck_Serializer_DTO_reponse = Truck_Serializer_DTO(base_DTO_obj)

                    return JsonResponse(truck_Serializer_DTO_reponse.data, status=status.HTTP_200_OK)

        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = e
            base_DTO_obj.data = None

            truck_Serializer_DTO_reponse = Truck_Serializer_DTO(base_DTO_obj)

        return JsonResponse(truck_Serializer_DTO_reponse.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'DELETE'])
def deleted_truck(request):

    if request.method == 'POST':

        try:

            truck_data = JSONParser().parse(request)
            truck_list = Truck.objects.filter(truck_license__in=truck_data)
            
            truck_list.update(is_active = False)

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "success"
            base_DTO_obj.massage = configMessage.configs.get("TRUCK_MASTER_DELETE_MASSAGE_SUCCESSFUL").data
            base_DTO_obj.data_list = None

            truck_list_serializer_DTO_reponse = Truck_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(truck_list_serializer_DTO_reponse.data, safe=False) 
            

        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = e
            base_DTO_obj.data = None

            truck_Serializer_DTO_reponse = Truck_Serializer_DTO(base_DTO_obj)

            return JsonResponse(truck_Serializer_DTO_reponse.data, safe=False)


@api_view(['GET', 'POST', 'DELETE'])
def edited_truck(request):

    if request.method == 'POST':

        try:

            truck_data = JSONParser().parse(request)     

            if truck_data['province'] is None or truck_data['province'].strip() == "" :

                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("TRUCK_MASTER_PROVINCE_REQUIRED").data
                base_DTO_obj.data = None

                truck_Serializer_DTO = Truck_Serializer_DTO(base_DTO_obj)

                return JsonResponse(truck_Serializer_DTO.data, status=status.HTTP_200_OK) 
            
            elif truck_data['truck_type'] is None or truck_data['truck_type'].strip() == "" :

                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("TRUCK_MASTER_TRUCKTYPE_REQUIRED").data
                base_DTO_obj.data = None

                truck_Serializer_DTO = Truck_Serializer_DTO(base_DTO_obj)

                return JsonResponse(truck_Serializer_DTO.data, status=status.HTTP_200_OK) 
            
            
            elif truck_data['fuel_type'] is None or truck_data['fuel_type'].strip() == "" :

                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("TRUCK_MASTER_FUELTYPE_REQUIRED").data
                base_DTO_obj.data = None

                truck_Serializer_DTO = Truck_Serializer_DTO(base_DTO_obj)

                return JsonResponse(truck_Serializer_DTO.data, status=status.HTTP_200_OK)
            
            elif truck_data['max_speed'] is None or truck_data['max_speed'] == "" :

                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("TRUCK_MASTER_MAXSPEED_REQUIRED").data
                base_DTO_obj.data = None

                truck_Serializer_DTO = Truck_Serializer_DTO(base_DTO_obj)

                return JsonResponse(truck_Serializer_DTO.data, status=status.HTTP_200_OK)
            
            elif truck_data['max_volume'] is None or truck_data['max_volume'] == "" :

                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("TRUCK_MASTER_MAXVOLUME_REQUIRED").data
                base_DTO_obj.data = None

                truck_Serializer_DTO = Truck_Serializer_DTO(base_DTO_obj)

                return JsonResponse(truck_Serializer_DTO.data, status=status.HTTP_200_OK)
            
            elif truck_data['max_weight'] is None or truck_data['max_weight'] == "" :

                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("TRUCK_MASTER_MAXWEIGHT_REQUIRED").data
                base_DTO_obj.data = None

                truck_Serializer_DTO = Truck_Serializer_DTO(base_DTO_obj)

                return JsonResponse(truck_Serializer_DTO.data, status=status.HTTP_200_OK)
            
            else :

                truck_obj = Truck.objects.filter( truck_license = truck_data["truck_license"] )
                truck_serializer_obj = Truck_Serializer(truck_obj[0],data=truck_data)

                if truck_serializer_obj.is_valid():

                    truck_serializer_obj.save()
                    

                    base_DTO_obj =  base_DTO()
                    base_DTO_obj.serviceStatus = "success"
                    base_DTO_obj.massage = configMessage.configs.get("TRUCK_MASTER_EDIT_MASSAGE_SUCCESSFUL").data  
                    base_DTO_obj.data_list = Truck.objects.all()

                    truck_list_serializer_DTO_reponse = Truck_list_Serializer_DTO(base_DTO_obj)

                    return JsonResponse(truck_list_serializer_DTO_reponse.data, safe=False) 

        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = e
            base_DTO_obj.data = None

            truck_Serializer_DTO_reponse = Truck_Serializer_DTO(base_DTO_obj)

            return JsonResponse(truck_Serializer_DTO_reponse.data, safe=False)


@api_view(['POST'])
def seach_truck(request):

    if request.method == 'POST':

        try:

            truck_data_obj = JSONParser().parse(request)

            truck_licese_str = truck_data_obj['truck_licese']
            truck_province_str = truck_data_obj['truck_province']
            truck_type_str = truck_data_obj['truck_type']
            truck_fuel_str = truck_data_obj['truck_fuel']

            print(truck_licese_str)
            print(truck_province_str)
            print(truck_type_str)
            print(truck_fuel_str)
            query = "select * from master_data_truck "

            joint_str = "" 
            where_str = " where 1 = 1 and master_data_truck.is_active = true "

            if truck_licese_str is not None and truck_licese_str != "" :

                truck_licese_str = "%"+truck_licese_str+"%"
                where_str = where_str + " and  master_data_truck.truck_license LIKE '%%%s%%'  " %  truck_licese_str

            if truck_province_str is not None and truck_province_str != "" :

                where_str = where_str + " and  UPPER(master_data_truck.province) = '%s' " % truck_province_str.upper()
            
            if truck_type_str is not None and truck_type_str != "" :

                where_str = where_str + " and  UPPER(master_data_truck.truck_type) = '%s' " % truck_type_str.upper()
            
            if truck_fuel_str is not None and truck_fuel_str != "" :

                where_str = where_str + " and  UPPER(master_data_truck.fuel_type) = '%s' " % truck_fuel_str.upper()
             
            query = query + joint_str + where_str + " Order By master_data_truck.updated_date desc"

            truck_list = Truck.objects.raw(query)

            truck_csv_list = []

            truck_csv_list.insert(0, [
                        "Truck License",
                        "Province",
                        "Truck Type",
                        "Fuel Type",
                        "Max Speed",
                        "Max Volume",
                        "Max Weight",
                        "Remark",
                        "Update By",
                        "Update Date",
                    ]
                )
            
            for truck_obj in truck_list:

                truck_row_list = (
                    truck_obj.truck_license,
                    truck_obj.province,
                    truck_obj.truck_type,
                    truck_obj.fuel_type,
                    truck_obj.max_speed,
                    truck_obj.max_volume,
                    truck_obj.max_weight,
                    truck_obj.remark,
                    truck_obj.updated_by,
                    truck_obj.updated_date.strftime("%d/%m/%Y"),

                    )
                
                truck_csv_list.append(truck_row_list)

            name_csv_str = "TruckCSV_" +datetime.now().strftime("%Y%m%d_%H%M%S")

            with open("media/" +  name_csv_str +'.csv', 'w', newline='',encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(truck_csv_list)
            
            truck_serializer = Truck_Serializer(truck_list, many=True)

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "success"
            base_DTO_obj.massage = "seach truck"
            base_DTO_obj.data_list = truck_serializer.data
            base_DTO_obj.csv_name =  name_csv_str + '.csv'

            truck_list_Serializer_DTO = Truck_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(truck_list_Serializer_DTO.data,safe=False)

        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = e
            base_DTO_obj.data = None

            truck_Serializer_DTO_reponse = Truck_Serializer_DTO(base_DTO_obj)

            return JsonResponse(truck_Serializer_DTO_reponse.data, safe=False)

@api_view(['GET', 'POST', 'DELETE'])
def driver_list(request):
    
    if request.method == 'GET':
        try:
            driver_list = Driver.objects.filter(is_active=True)
            driver_serializer_obj = Driver_Serializer(driver_list, many=True)

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "success"
            base_DTO_obj.massage = "get driver"
            base_DTO_obj.data_list = driver_serializer_obj.data

            driver_list_Serializer_DTO_obj = Driver_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(driver_list_Serializer_DTO_obj.data, status=status.HTTP_200_OK)
        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "error"
            base_DTO_obj.massage = e 
            # base_DTO_obj.data_list = order_serializer.data

            driver_list_Serializer_DTO_obj = Driver_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(driver_list_Serializer_DTO_obj.data, status=status.HTTP_200_OK)

        

            # return JsonResponse(order_serializer.data, safe=False)

    elif request.method == 'POST':


        try:
            driver_data = JSONParser().parse(request)

            if driver_data['driver_code'] is None or driver_data['driver_code'].strip() == "" :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("DRIVER_MASTER_DRIVERCODE_REQUIRED").data
                base_DTO_obj.data = None

                driver_Serializer_DTO = Driver_Serializer_DTO(base_DTO_obj)

                return JsonResponse(driver_Serializer_DTO.data, status=status.HTTP_200_OK) 
            
            elif driver_data['name'] is None or driver_data['name'].strip() == "" :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("DRIVER_MASTER_DRIVERNAME_REQUIRED").data
                base_DTO_obj.data = None

                driver_Serializer_DTO = Driver_Serializer_DTO(base_DTO_obj)

                return JsonResponse(driver_Serializer_DTO.data, status=status.HTTP_200_OK) 
            
            elif driver_data['tel'] is None or driver_data['tel'].strip() == "" :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error" 
                base_DTO_obj.massage = configMessage.configs.get("DRIVER_MASTER_DRIVERTEL_REQUIRED").data
                base_DTO_obj.data = None

                driver_Serializer_DTO = Driver_Serializer_DTO(base_DTO_obj)

                return JsonResponse(driver_Serializer_DTO.data, status=status.HTTP_200_OK) 
            
            else :
                 
                driver_list = Driver.objects.filter(driver_code = driver_data['driver_code'])
                
                if len(driver_list) >0 :

                    if driver_list[0].is_active :
                        base_DTO_obj =  base_DTO()
                        base_DTO_obj.serviceStatus = "Error"
                        base_DTO_obj.massage = configMessage.configs.get("DRIVER_MASTER_DUPLICATE").data
                        base_DTO_obj.data = None

                        driver_Serializer_DTO_reponse = Driver_Serializer_DTO(base_DTO_obj)

                        return JsonResponse(driver_Serializer_DTO_reponse.data, status=status.HTTP_200_OK) 
                    
                    else :
                        
                        driver_list.update(
                            name=driver_data['name'],
                            tel=driver_data['tel'],
                            remark=driver_data['remark'],
                            is_active=True
                        )

                        base_DTO_obj =  base_DTO()
                        base_DTO_obj.serviceStatus = "success"
                        base_DTO_obj.massage = configMessage.configs.get("DRIVER_MASTER_ADD_MASSAGE_SUCCESSFUL").data
                        base_DTO_obj.data = None

                        driver_Serializer_DTO_reponse = Driver_Serializer_DTO(base_DTO_obj)

                        return JsonResponse(driver_Serializer_DTO_reponse.data, status=status.HTTP_200_OK)

                driver_serializer_obj = Driver_Serializer(data=driver_data)

                if driver_serializer_obj.is_valid():
                    
                    driver_serializer_obj.save()
                    base_DTO_obj =  base_DTO()
                    base_DTO_obj.serviceStatus = "success"
                    base_DTO_obj.massage = configMessage.configs.get("DRIVER_MASTER_ADD_MASSAGE_SUCCESSFUL").data
                    base_DTO_obj.data = driver_serializer_obj.data

                    driver_Serializer_DTO_reponse = Driver_Serializer_DTO(base_DTO_obj)

                    return JsonResponse(driver_Serializer_DTO_reponse.data, status=status.HTTP_200_OK) 
                
                else : 

                    base_DTO_obj =  base_DTO()
                    base_DTO_obj.serviceStatus = "Error"
                    base_DTO_obj.massage = driver_serializer_obj.errors
                    base_DTO_obj.data = None

                    driver_Serializer_DTO_reponse = Driver_Serializer_DTO(base_DTO_obj)

                    return JsonResponse(driver_Serializer_DTO_reponse.data, status=status.HTTP_200_OK)

        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = e
            base_DTO_obj.data = None

            driver_Serializer_DTO_reponse = Driver_Serializer_DTO(base_DTO_obj)

        return JsonResponse(driver_Serializer_DTO_reponse.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST', 'DELETE'])
def deleted_driver(request):

    if request.method == 'POST':

        try:

            driver_data = JSONParser().parse(request)
            driver_list = Driver.objects.filter(driver_code__in=driver_data)
            
            driver_list.update(is_active = False)

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "success"
            base_DTO_obj.massage = configMessage.configs.get("DRIVER_MASTER_DELETE_MASSAGE_SUCCESSFUL").data
            base_DTO_obj.data_list = None

            driver_list_serializer_DTO_reponse = Driver_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(driver_list_serializer_DTO_reponse.data, safe=False) 
            

        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage =  e
            base_DTO_obj.data = None

            driver_Serializer_DTO_reponse = Driver_Serializer_DTO(base_DTO_obj)

            return JsonResponse(driver_Serializer_DTO_reponse.data, safe=False)


@api_view(['GET', 'POST', 'DELETE'])
def edited_driver(request):

    if request.method == 'POST':

        try:

            driver_data = JSONParser().parse(request)

            if driver_data['driver_code'] is None or driver_data['driver_code'].strip() == "" :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage =  configMessage.configs.get("DRIVER_MASTER_DRIVERCODE_REQUIRED").data
                base_DTO_obj.data = None

                driver_Serializer_DTO = Driver_Serializer_DTO(base_DTO_obj)

                return JsonResponse(driver_Serializer_DTO.data, status=status.HTTP_200_OK) 
            
            elif driver_data['name'] is None or driver_data['name'].strip() == "" :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("DRIVER_MASTER_DRIVERNAME_REQUIRED").data
                base_DTO_obj.data = None

                driver_Serializer_DTO = Driver_Serializer_DTO(base_DTO_obj)

                return JsonResponse(driver_Serializer_DTO.data, status=status.HTTP_200_OK) 
            
            elif driver_data['tel'] is None or driver_data['tel'].strip() == "" :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("DRIVER_MASTER_DRIVERTEL_REQUIRED").data
                base_DTO_obj.data = None

                driver_Serializer_DTO = Driver_Serializer_DTO(base_DTO_obj)

                return JsonResponse(driver_Serializer_DTO.data, status=status.HTTP_200_OK) 
            
            else :
                driver_obj = Driver.objects.filter( driver_code = driver_data["driver_code"] )

                driver_serializer_obj = Driver_Serializer(driver_obj[0],data=driver_data)

                if driver_serializer_obj.is_valid():

                    driver_serializer_obj.save()
                    

                    base_DTO_obj =  base_DTO()
                    base_DTO_obj.serviceStatus = "success"
                    base_DTO_obj.massage = configMessage.configs.get("DRIVER_MASTER_EDIT_MASSAGE_SUCCESSFUL").data
                    base_DTO_obj.data_list = Driver.objects.all()

                    driver_list_serializer_DTO_reponse = Driver_list_Serializer_DTO(base_DTO_obj)

                    return JsonResponse(driver_list_serializer_DTO_reponse.data, safe=False) 
                
        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = e
            base_DTO_obj.data = None

            Driver_Serializer_DTO_reponse = Driver_Serializer_DTO(base_DTO_obj)

            return JsonResponse(Driver_Serializer_DTO_reponse.data, safe=False)

@api_view(['POST'])
def seach_driver(request):

    if request.method == 'POST':

        try:

            driver_data_obj = JSONParser().parse(request)

            driver_code_str = driver_data_obj['driver_code']
            driver_name_str = driver_data_obj['driver_name']

            query = "select * from master_data_driver "

            joint_str = "" 
            where_str = " where 1 = 1 and master_data_driver.is_active = true "

            if driver_code_str is not None:

                driver_code_str = "%"+driver_code_str+"%"
                where_str = where_str + " and  master_data_driver.driver_code LIKE '%%%s%%'  " %  driver_code_str 
            
            if driver_name_str is not None :

                driver_name_str = "%"+driver_name_str+"%"
                where_str = where_str + " and  master_data_driver.name LIKE '%%%s%%'  " %  driver_name_str 

            
            query = query + joint_str + where_str + " Order by updated_date desc"

            driver_list = Driver.objects.raw(query)

            driver_csv_list = []

            driver_csv_list.insert(0, [
                        "Driver Code",
                        "Driver Name",
                        "Driver Tel",
                        "Remark",
                        "Updated By",
                        "Updated Date"
                    ]
                )
            
            for driver_obj in driver_list:

                driver_row_list = (
                    driver_obj.driver_code,
                    driver_obj.name,
                    driver_obj.tel,
                    driver_obj.remark,
                    driver_obj.updated_by,
                    driver_obj.updated_date.strftime("%d/%m/%Y"),

                    )
                
                driver_csv_list.append(driver_row_list)

            name_csv_str = "DriverMasterCSV" +datetime.now().strftime("%Y%m%d_%H%M%S")

            with open("media/" +  name_csv_str +'.csv', 'w', newline='',encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(driver_csv_list)
            
            
            
            driver_serializer = Driver_Serializer(driver_list, many=True)

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "success"
            base_DTO_obj.massage = "seach driver"
            base_DTO_obj.data_list = driver_serializer.data
            base_DTO_obj.csv_name =  name_csv_str + '.csv'

            driver_list_Serializer_DTO = Driver_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(driver_list_Serializer_DTO.data,safe=False)

        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = e
            base_DTO_obj.data = None

            driver_Serializer_DTO_reponse = Truck_Serializer_DTO(base_DTO_obj)

            return JsonResponse(driver_Serializer_DTO_reponse.data, safe=False)

@api_view(['POST'])
def search_route_master(request):

    if request.method == 'POST':

        try:
            customer_code_selected = request.data['customer_code_selected']
            project_code_selected = request.data['project_code_selected']
            supplier_code_selected = request.data['supplier_code_selected']
            plant_code_selected = request.data['plant_code_selected']
            route_code_selected = request.data['route_code_selected']
            trip_no_selected = request.data['trip_no_selected']

            print(request.data['trip_no_selected'])

            query = "select * from master_data_routermaster "

            joint_str = "" 
            where_str = " where 1 = 1   and  master_data_routermaster.is_active = true "


            if customer_code_selected is not None:

                joint_str = joint_str + " INNER JOIN master_data_project "
                joint_str = joint_str + " ON UPPER(master_data_project.project_code) = UPPER(master_data_routermaster.project_code) "
                joint_str = joint_str + " INNER JOIN master_data_customer "
                joint_str = joint_str + " ON UPPER(master_data_customer.customer_code) = UPPER(master_data_project.customer_code) "
                where_str = where_str + " and  UPPER(master_data_customer.customer_code) = '%s' " % customer_code_selected.upper()
                    
            if project_code_selected is not None:

                where_str = where_str + " and  UPPER(master_data_routermaster.project_code) = '%s' " % project_code_selected.upper()

            if supplier_code_selected is not None:

                where_str = where_str + " and  UPPER(master_data_routermaster.supplier_code) = '%s' " % supplier_code_selected.upper()
            
            if plant_code_selected is not None:

                where_str = where_str + " and  UPPER(master_data_routermaster.plant_code) = '%s' " % plant_code_selected.upper()
            
            if route_code_selected is not None:

                where_str = where_str + " and  UPPER(master_data_routermaster.route_code) = '%s' " % route_code_selected.upper()
            
            if trip_no_selected is not None:

                where_str = where_str + " and  UPPER(master_data_routermaster.trip_no) = '%s' " % trip_no_selected.upper()
            
            query = query + joint_str + where_str + " order by master_data_routermaster.updated_date desc"

            print(query)

            routerMaster_list = RouterMaster.objects.raw(query)



            routerMaster_csv_list = []

            routerMaster_csv_list.insert(0, [
                "Customer",
                "Project Code",
                "Route Code",
                "Trip No",
                "Supplier Code",
                "Plant Code",
                "Pickup Before",
                "Release Time",
                "Pickup Time",
                "Depart Time",
                "Delivery Time",
                "Complete Time",
                "Update by",
                "Update Date"
                ]
            )

            route_master_dto_list = []
            for routerMaster_obj in routerMaster_list:

                print(routerMaster_obj.project_code)
                route_master_dto_obj =  RouteMasterDTO()
                route_master_dto_obj.route_no = routerMaster_obj.route_no
                route_master_dto_obj.customer_code = Project.objects.get(project_code__iexact=routerMaster_obj.project_code).customer_code
                route_master_dto_obj.project_code = routerMaster_obj.project_code
                route_master_dto_obj.route_code = routerMaster_obj.route_code
                route_master_dto_obj.trip_no = routerMaster_obj.trip_no
                route_master_dto_obj.supplier_code = routerMaster_obj.supplier_code
                route_master_dto_obj.plant_code = routerMaster_obj.plant_code
                route_master_dto_obj.pickup_before = routerMaster_obj.pickup_before
                route_master_dto_obj.release_time = formal_decimal(routerMaster_obj.release_time)
                route_master_dto_obj.pickup_time = formal_decimal(routerMaster_obj.pickup_time)
                route_master_dto_obj.depart_time = formal_decimal(routerMaster_obj.depart_time)
                route_master_dto_obj.delivery_time = formal_decimal(routerMaster_obj.delivery_time)
                route_master_dto_obj.complete_time = formal_decimal(routerMaster_obj.complete_time)
                route_master_dto_obj.updated_by = routerMaster_obj.updated_by
                route_master_dto_obj.updated_date = routerMaster_obj.updated_date
            
                route_master_dto_list.append(route_master_dto_obj)

                route_master_row_list = (
                                route_master_dto_obj.customer_code,
                                route_master_dto_obj.project_code,
                                route_master_dto_obj.route_code,
                                route_master_dto_obj.trip_no,
                                route_master_dto_obj.supplier_code,
                                route_master_dto_obj.plant_code,
                                route_master_dto_obj.pickup_before,
                                formal_decimal(route_master_dto_obj.release_time),
                                formal_decimal(route_master_dto_obj.pickup_time),
                                formal_decimal(route_master_dto_obj.depart_time),
                                formal_decimal(route_master_dto_obj.delivery_time),
                                formal_decimal(route_master_dto_obj.complete_time),
                                route_master_dto_obj.updated_by,
                                route_master_dto_obj.updated_date.strftime("%d/%m/%Y")

                                )

                routerMaster_csv_list.append(route_master_row_list)

            name_csv_str = "RouterMasterCSV" +datetime.now().strftime("%Y%m%d_%H%M%S")

            with open("media/" +  name_csv_str +'.csv', 'w', newline='',encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(routerMaster_csv_list)
            
            route_serializer = RouterMaster_Serializer(route_master_dto_list, many=True)


            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "success"
            base_DTO_obj.massage = "get part"
            base_DTO_obj.data_list = route_serializer.data
            base_DTO_obj.csv_name =  name_csv_str + '.csv'

            router_master_list_Serializer_DTO = RouterMaster_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(router_master_list_Serializer_DTO.data, safe=False)

        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = e
            base_DTO_obj.data = None

            router_master_list_Serializer_DTO = RouterMaster_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(router_master_list_Serializer_DTO.data, safe=False)

def formal_decimal(number_str):

    number_array = number_str.split(".")

    print(number_array)
    if len(number_array[0]) == 1 :

        number_array[0] =  "0" + number_array[0] 

    if len(number_array[1]) == 1 :

        number_array[1] =  number_array[1] +"0" 

    return number_array[0] +"."+ number_array[1]


@api_view(['GET', 'POST', 'DELETE'])
def routeMaster_list(request):
    
    if request.method == 'GET':
        try:
            routerMaster_list = RouterMaster.objects.filter(is_active=True)
            routerMaster_serializer_obj = RouterMaster_Serializer(routerMaster_list, many=True)

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "success"
            base_DTO_obj.massage = "get routerMaster"
            base_DTO_obj.data_list = routerMaster_serializer_obj.data

            routerMaster_list_Serializer_DTO_obj = RouterMaster_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(routerMaster_list_Serializer_DTO_obj.data, status=status.HTTP_200_OK)
        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "error"
            base_DTO_obj.massage = e 
            # base_DTO_obj.data_list = order_serializer.data

            routerMaster_list_Serializer_DTO_obj = RouterMaster_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(routerMaster_list_Serializer_DTO_obj.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':

        try:
            routerMaster_data = JSONParser().parse(request)
            print("dfsdfsdfsdfsdf")
            print(routerMaster_data)
            time_rex = re.compile("([0-2]|""){1}[0-9]{1}[.][0-5]{1}[0-9]{1}")

            if routerMaster_data['project_code'] is None or routerMaster_data['project_code'].strip() == "" :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("ROUTE_MASTER_PROJECTCODE_REQUIRED").data
                base_DTO_obj.data = None

                routerMaster_Serializer_DTO_reponse = RouterMaster_Serializer_DTO(base_DTO_obj)

                return JsonResponse(routerMaster_Serializer_DTO_reponse.data, status=status.HTTP_200_OK) 
            
            elif routerMaster_data['route_code'] is None or routerMaster_data['route_code'].strip() == "" :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("ROUTE_MASTER_ROUTECODE_REQUIRED").data
                base_DTO_obj.data = None

                routerMaster_Serializer_DTO_reponse = RouterMaster_Serializer_DTO(base_DTO_obj)

                return JsonResponse(routerMaster_Serializer_DTO_reponse.data, status=status.HTTP_200_OK) 

            elif routerMaster_data['trip_no'] is None or routerMaster_data['trip_no'].strip() == "" :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("ROUTE_MASTER_TRIPNO_REQUIRED").data
                base_DTO_obj.data = None

                routerMaster_Serializer_DTO_reponse = RouterMaster_Serializer_DTO(base_DTO_obj)

                return JsonResponse(routerMaster_Serializer_DTO_reponse.data, status=status.HTTP_200_OK) 
            
            elif routerMaster_data['supplier_code'] is None or routerMaster_data['supplier_code'].strip() == "" :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("ROUTE_MASTER_SUPPLIERCODE_REQUIRED").data
                base_DTO_obj.data = None

                routerMaster_Serializer_DTO_reponse = RouterMaster_Serializer_DTO(base_DTO_obj)

                return JsonResponse(routerMaster_Serializer_DTO_reponse.data, status=status.HTTP_200_OK) 
            
            elif routerMaster_data['plant_code'] is None or routerMaster_data['plant_code'].strip() == "" :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("ROUTE_MASTER_PLANTCODE_REQUIRED").data
                base_DTO_obj.data = None

                routerMaster_Serializer_DTO_reponse = RouterMaster_Serializer_DTO(base_DTO_obj)

                return JsonResponse(routerMaster_Serializer_DTO_reponse.data, status=status.HTTP_200_OK)
            
            elif routerMaster_data['pickup_before'] is None or routerMaster_data['pickup_before'] == "" :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("ROUTE_MASTER_PICKUPBEFORE_REQUIRED").data
                base_DTO_obj.data = None

                routerMaster_Serializer_DTO_reponse = RouterMaster_Serializer_DTO(base_DTO_obj)

                return JsonResponse(routerMaster_Serializer_DTO_reponse.data, status=status.HTTP_200_OK)
            
            elif routerMaster_data['release_time'] is None or routerMaster_data['release_time'].strip() == "" :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("ROUTE_MASTER_RELEASETIME_REQUIRED").data
                base_DTO_obj.data = None

                routerMaster_Serializer_DTO_reponse = RouterMaster_Serializer_DTO(base_DTO_obj)

                return JsonResponse(routerMaster_Serializer_DTO_reponse.data, status=status.HTTP_200_OK)

            elif not time_rex.match(routerMaster_data['release_time'] ) :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("ROUTE_MASTER_RELEASETIME_INCORRECT_FORMAT").data
                base_DTO_obj.data = None

                routerMaster_Serializer_DTO_reponse = RouterMaster_Serializer_DTO(base_DTO_obj)

                return JsonResponse(routerMaster_Serializer_DTO_reponse.data, status=status.HTTP_200_OK)
            
            elif routerMaster_data['pickup_time'] is None or routerMaster_data['pickup_time'].strip() == "" :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("ROUTE_MASTER_PICKUPTIME_REQUIRED").data
                base_DTO_obj.data = None

                routerMaster_Serializer_DTO_reponse = RouterMaster_Serializer_DTO(base_DTO_obj)

                return JsonResponse(routerMaster_Serializer_DTO_reponse.data, status=status.HTTP_200_OK)
            
            elif not time_rex.match(routerMaster_data['pickup_time'] ) :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("ROUTE_MASTER_PICKUPTIME_INCORRECT_FORMAT").data
                base_DTO_obj.data = None

                routerMaster_Serializer_DTO_reponse = RouterMaster_Serializer_DTO(base_DTO_obj)

                return JsonResponse(routerMaster_Serializer_DTO_reponse.data, status=status.HTTP_200_OK)
            
            elif routerMaster_data['depart_time'] is None or routerMaster_data['depart_time'].strip() == "" :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("ROUTE_MASTER_DEPARTTIME_REQUIRED").data
                base_DTO_obj.data = None

                routerMaster_Serializer_DTO_reponse = RouterMaster_Serializer_DTO(base_DTO_obj)

                return JsonResponse(routerMaster_Serializer_DTO_reponse.data, status=status.HTTP_200_OK)
            
            elif not time_rex.match(routerMaster_data['depart_time'] ) :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("ROUTE_MASTER_DEPARTTIME_INCORRECT_FORMAT").data
                base_DTO_obj.data = None

                routerMaster_Serializer_DTO_reponse = RouterMaster_Serializer_DTO(base_DTO_obj)

                return JsonResponse(routerMaster_Serializer_DTO_reponse.data, status=status.HTTP_200_OK)
            
            elif routerMaster_data['delivery_time'] is None or routerMaster_data['delivery_time'].strip() == "" :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("ROUTE_MASTER_DELIVERYTIME_REQUIRED").data
                base_DTO_obj.data = None

                routerMaster_Serializer_DTO_reponse = RouterMaster_Serializer_DTO(base_DTO_obj)

                return JsonResponse(routerMaster_Serializer_DTO_reponse.data, status=status.HTTP_200_OK)
            
            elif not time_rex.match(routerMaster_data['delivery_time'] ) :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("ROUTE_MASTER_DELIVERYTIME_INCORRECT_FORMAT").data
                base_DTO_obj.data = None

                routerMaster_Serializer_DTO_reponse = RouterMaster_Serializer_DTO(base_DTO_obj)

                return JsonResponse(routerMaster_Serializer_DTO_reponse.data, status=status.HTTP_200_OK)
            
            elif routerMaster_data['complete_time'] is None or routerMaster_data['complete_time'].strip() == "" :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("ROUTE_MASTER_COMPLETETIME_REQUIRED").data
                base_DTO_obj.data = None

                routerMaster_Serializer_DTO_reponse = RouterMaster_Serializer_DTO(base_DTO_obj)

                return JsonResponse(routerMaster_Serializer_DTO_reponse.data, status=status.HTTP_200_OK)
            
            elif not time_rex.match(routerMaster_data['complete_time'] ) :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("ROUTE_MASTER_COMPLETETIME_INCORRECT_FORMAT").data
                base_DTO_obj.data = None

                routerMaster_Serializer_DTO_reponse = RouterMaster_Serializer_DTO(base_DTO_obj)

                return JsonResponse(routerMaster_Serializer_DTO_reponse.data, status=status.HTTP_200_OK)
            
            else : 

                route_no_str = routerMaster_data['route_code'] + "-" + routerMaster_data['trip_no'] + "-" + routerMaster_data['supplier_code'] + "-" + routerMaster_data['plant_code']
                route_no_str = route_no_str.upper()
                routerMaster_data['release_time'] = formal_decimal(routerMaster_data['release_time'])
                routerMaster_data['pickup_time'] = formal_decimal(routerMaster_data['pickup_time'])
                routerMaster_data['depart_time'] = formal_decimal(routerMaster_data['depart_time'])
                routerMaster_data['delivery_time'] = formal_decimal(routerMaster_data['delivery_time'])
                routerMaster_data['complete_time'] = formal_decimal(routerMaster_data['complete_time'])

                routerMaster_list = RouterMaster.objects.filter(route_no = route_no_str)
                routerMaster_data['route_no'] = route_no_str
                router_master_serializer_obj = RouterMaster_Serializer(data=routerMaster_data)

                
                if router_master_serializer_obj.is_valid():

                    router_master_serializer_obj.save()
                    
                    base_DTO_obj =  base_DTO()
                    base_DTO_obj.serviceStatus = "success"
                    base_DTO_obj.massage = configMessage.configs.get("ROUTE_MASTER_ADD_MASSAGE_SUCCESSFUL").data
                    base_DTO_obj.data = router_master_serializer_obj.data

                    router_master_serializer_DTO_reponse = RouterMaster_Serializer_DTO(base_DTO_obj)

                    return JsonResponse(router_master_serializer_DTO_reponse.data, status=status.HTTP_201_CREATED) 
                
                else : 
                    base_DTO_obj =  base_DTO()
                    base_DTO_obj.serviceStatus = "Error"
                    base_DTO_obj.massage = router_master_serializer_obj.errors[list(router_master_serializer_obj.errors)[0]][0]
                    base_DTO_obj.data = None
                
                    router_master_serializer_DTO_reponse = RouterMaster_Serializer_DTO(base_DTO_obj)

                    return JsonResponse(router_master_serializer_DTO_reponse.data, status=status.HTTP_201_CREATED)

        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = e
            base_DTO_obj.data = None

            router_master_serializer_DTO_reponse = RouterMaster_Serializer_DTO(base_DTO_obj)

        return JsonResponse(router_master_serializer_DTO_reponse.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def upload_route_master(request):
    
    if request.method == 'POST':

        try:
            
            
            file_serializer = File_Serializer(data=request.data)
        
            if file_serializer.is_valid():

              
                upload_route_master_file = request.FILES['file']
                fs = FileSystemStorage(location="media/") #defaults to   MEDIA_ROOT  
                file_name_str = fs.save(upload_route_master_file.name, upload_route_master_file)
                
                routerMaster_list = []
                validateError_list = []
                validateWarning_list = []

                with open("media/" +file_name_str, newline='') as csvfile:
                    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                    row_int = 0
                    
                    for row in spamreader:
                       
                        if row_int > 0 :
                            routerMaster_obj =  RouteMasterDTO()
                            
                         

                            if not str(row[0]) :
                                    validateError_obj = validateError()
                                    validateError_obj.error = configMessage.configs.get("ROUTE_MASTER_CUSTOMERCODE_REQUIRED").data  
                                    validateError_obj.row = row_int + 1
                                    validateError_obj.column = 1
                                    validateError_list.append(validateError_obj)
                                
                            else : 
                                    
                                customer_list = Customer.objects.filter(customer_code__iexact = str(row[0]))
                                if len(customer_list) <=0 :
                                        
                                    validateError_obj = validateError()
                                    validateError_obj.error = configMessage.configs.get("ROUTE_MASTER_CUSTOMERCODE_EXISTING").data  
                                    validateError_obj.row = row_int + 1
                                    validateError_obj.column = 1
                                    validateError_list.append(validateError_obj)

                                else :

                                    routerMaster_obj.customer_code = str(row[0])

    
                            if not str(row[1]) :

                                    validateError_obj = validateError()
                                    validateError_obj.error = configMessage.configs.get("ROUTE_MASTER_PROJECTCODE_REQUIRED").data
                                    validateError_obj.row = row_int + 1
                                    validateError_obj.column = 2
                                    validateError_list.append(validateError_obj)
                                
                            else : 
                                project_list = Project.objects.filter(project_code__iexact = str(row[1]))
                                    
                                if len(project_list) <=0 :

                                    validateError_obj = validateError()
                                    validateError_obj.error = configMessage.configs.get("ROUTE_MASTER_PROJECTCODE_EXISTING").data
                                    validateError_obj.row = row_int + 1
                                    validateError_obj.column = 2
                                    validateError_list.append(validateError_obj)

                                else :

                                    routerMaster_obj.project_code = str(row[1])
                                
                            if not str(row[2]) :

                                validateError_obj = validateError()
                                validateError_obj.error = configMessage.configs.get("ROUTE_MASTER_ROUTECODE_REQUIRED").data
                                validateError_obj.row = row_int + 1
                                validateError_obj.column = 3
                                validateError_list.append(validateError_obj)
                                
                            else : 
                                    
                                routerMaster_obj.route_code = str(row[2])
                            
                            if not str(row[3]) :

                                validateError_obj = validateError()
                                validateError_obj.error = configMessage.configs.get("ROUTE_MASTER_TRIPNO_REQUIRED").data
                                validateError_obj.row = row_int + 1
                                validateError_obj.column = 4
                                validateError_list.append(validateError_obj)
                                
                            else : 
                                    
                                routerMaster_obj.trip_no = str(row[3])
                            
                            RouterMaster_list = RouterMaster.objects.filter(route_code__iexact=str(row[2]),trip_no__iexact=str(row[3]),supplier_code__iexact=str(row[4]),plant_code__iexact=str(row[5]))

                            if len(RouterMaster_list) > 0 : 

                                routerMaster_obj.is_update = True

                            if not str(row[4]) :

                                    validateError_obj = validateError()
                                    validateError_obj.error = configMessage.configs.get("ROUTE_MASTER_SUPPLIERCODE_REQUIRED").data
                                    validateError_obj.row = row_int + 1
                                    validateError_obj.column = 5
                                    validateError_list.append(validateError_obj)

                                
                            else : 
                                    
                                # routerMaster_obj.supplier_code = str(row[4])
                                supplier_list = Station.objects.filter(station_code__iexact=str(row[4]).strip(),station_type__iexact="SUPPLIER",is_active=True)
                                if len(supplier_list) <=0 :

                                    validateError_obj = validateError()
                                    validateError_obj.error = configMessage.configs.get("ROUTE_MASTER_SUPPLIERCODE_EXISTING").data
                                    validateError_obj.row = row_int + 1
                                    validateError_obj.column = 5
                                    validateError_list.append(validateError_obj)

                                else :

                                    routerMaster_obj.supplier_code = str(row[4])
                                

                            if not str(row[5]) :

                                    validateError_obj = validateError()
                                    validateError_obj.error = configMessage.configs.get("ROUTE_MASTER_PLANTCODE_REQUIRED").data
                                    validateError_obj.row = row_int + 1
                                    validateError_obj.column = 5
                                    validateError_list.append(validateError_obj)
                                
                            else : 
                                    
                                plant_list = Station.objects.filter(station_code__iexact=str(row[5]).strip(),station_type__iexact="PLANT",is_active=True)
                                    
                                if len(plant_list) <=0 :

                                    validateError_obj = validateError()
                                    validateError_obj.error = configMessage.configs.get("ROUTE_MASTER_PLANTCODE_EXISTING").data
                                    validateError_obj.row = row_int + 1
                                    validateError_obj.column = 6
                                    validateError_list.append(validateError_obj)

                                else :

                                    routerMaster_obj.plant_code = str(row[5])
                            
                      
                            if  not row[6].isdigit() :
                                
                                validateError_obj = validateError()
                                validateError_obj.error = configMessage.configs.get("ROUTE_MASTER_PICKUPBEFORE_INTEGER").data
                                validateError_obj.row = row_int + 1
                                validateError_obj.column = 7
                                validateError_list.append(validateError_obj)
                            else :

                                routerMaster_obj.pickup_before = row[6]
                            
                            rex = re.compile("([0-2]|""){1}[0-9]{1}[.][0-5]{1}")

                            if  not isinstance(row[7], int) :
    
                                if rex.match(str(row[7])):
                                    routerMaster_obj.release_time = str(row[7])
                                else:

                                    validateError_obj = validateError()
                                    validateError_obj.error = configMessage.configs.get("ROUTE_MASTER_RELEASETIME_INCORRECT_FORMAT").data
                                    validateError_obj.row = row_int + 1
                                    validateError_obj.column = 8
                                    validateError_list.append(validateError_obj)

                            if  not isinstance(row[8], int) :
    
                                if rex.match(str(row[8])):
                                    routerMaster_obj.pickup_time = str(row[8])
                                else:

                                    validateError_obj = validateError()
                                    validateError_obj.error = configMessage.configs.get("ROUTE_MASTER_PICKUPTIME_INCORRECT_FORMAT").data
                                    validateError_obj.row = row_int + 1
                                    validateError_obj.column = 9
                                    validateError_list.append(validateError_obj)
                            
                            if  not isinstance(row[9], int) :
    
                                if rex.match(str(row[9])):
                                    routerMaster_obj.depart_time = str(row[9])
                                else:

                                    validateError_obj = validateError()
                                    validateError_obj.error = configMessage.configs.get("ROUTE_MASTER_DEPARTTIME_INCORRECT_FORMAT").data
                                    validateError_obj.row = row_int + 1
                                    validateError_obj.column = 10
                                    validateError_list.append(validateError_obj)
                            
                            if  not isinstance(row[10], int) :
    
                                if rex.match(str(row[10])):
                                    routerMaster_obj.delivery_time = str(row[10])
                                else:

                                    validateError_obj = validateError()
                                    validateError_obj.error = configMessage.configs.get("ROUTE_MASTER_DELIVERYTIME_INCORRECT_FORMAT").data
                                    validateError_obj.row = row_int + 1
                                    validateError_obj.column = 11
                                    validateError_list.append(validateError_obj)
                            
                            if  not isinstance(row[11], int) :
    
                                if rex.match(str(row[11])):
                                    routerMaster_obj.complete_time = str(row[11])

                                else :

                                    validateError_obj = validateError()
                                    validateError_obj.error = configMessage.configs.get("ROUTE_MASTER_COMPLETETIME_INCORRECT_FORMAT").data
                                    validateError_obj.row = row_int + 1
                                    validateError_obj.column = 12
                                    validateError_list.append(validateError_obj)

                            routerMaster_list.append(routerMaster_obj)

                        row_int = row_int + 1

            
            if len(validateError_list) <= 0:

                row_int = 0
                
                for routerMaster_obj in routerMaster_list:
                    row_int = row_int +1
                    
                    if routerMaster_obj.is_update :
                        
                        routeMaster_update = RouterMaster.objects.filter(route_code__iexact=routerMaster_obj.route_code,trip_no__iexact=routerMaster_obj.trip_no,supplier_code__iexact=routerMaster_obj.supplier_code,plant_code__iexact=routerMaster_obj.plant_code)[0]
                        routeMaster_update.pickup_before = int(routerMaster_obj.pickup_before)
                        routeMaster_update.release_time = formal_decimal(routerMaster_obj.release_time)
                        routeMaster_update.pickup_time = formal_decimal(routerMaster_obj.pickup_time)
                        routeMaster_update.depart_time = formal_decimal(routerMaster_obj.depart_time)
                        routeMaster_update.delivery_time = formal_decimal(routerMaster_obj.delivery_time)
                        routeMaster_update.complete_time = formal_decimal(routerMaster_obj.complete_time)
                        routeMaster_update.updated_by = request.user.username
                        routeMaster_update.updated_date = datetime.utcnow()
                        routeMaster_update.is_active = True
                        routeMaster_update.save()

                    else :
                        
                        validate_warning_serializer_obj =  validate_warning_serializer()
                        validate_warning_serializer_obj.error = configMessage.configs.get("ROUTE_MASTER_EXISTING").data
                        validate_warning_serializer_obj.row = row_int + 1
                        validateWarning_list.append(validate_warning_serializer_obj)

                    
            validate_error_list_serializer = validate_error_serializer(validateError_list, many=True)   
            validate_warning_list_serializer = validate_warning_serializer(validateWarning_list, many=True)   
            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "success"
            base_DTO_obj.massage = configMessage.configs.get("ROUTE_INFO_EDIT_MASSAGE_SUCCESSFUL").data
            base_DTO_obj.data_list = None
            base_DTO_obj.validate_error_list =  validate_error_list_serializer.data
            base_DTO_obj.validate_warning_list = validate_warning_list_serializer.data

            router_master_list_Serializer_DTO = RouterMaster_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(router_master_list_Serializer_DTO.data, safe=False)            


 
        
        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "error"
            base_DTO_obj.massage = e
            base_DTO_obj.data_list = None
            base_DTO_obj.validate_error_list =  None

            router_master_list_Serializer_DTO = RouterMaster_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(router_master_list_Serializer_DTO.data, safe=False)

@api_view(['GET', 'POST', 'DELETE'])
def deleted_routeMaster(request):

    if request.method == 'POST':

        try:

            routeMaster_data = JSONParser().parse(request)
            print(routeMaster_data)
            routeMaster_list = RouterMaster.objects.filter(route_no__in=routeMaster_data)
            routeMaster_list.update(is_active = False)

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "success"
            base_DTO_obj.massage = configMessage.configs.get("ROUTE_MASTER_DELETE_MASSAGE_SUCCESSFUL").data
            base_DTO_obj.data_list = RouterMaster.objects.all()

            routerMaster_list_serializer_DTO_reponse = RouterMaster_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(routerMaster_list_serializer_DTO_reponse.data, safe=False) 

        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = e
            base_DTO_obj.data = None

            routerMaster_Serializer_DTO_reponse = RouterMaster_Serializer_DTO(base_DTO_obj)

            return JsonResponse(routerMaster_Serializer_DTO_reponse.data, safe=False)


@api_view(['GET', 'POST', 'DELETE'])
def routeInfo_list(request):
    
    if request.method == 'GET':
        try:
            routerInfo_list = RouterInfo.objects.filter(is_active=True)
            routerInfo_serializer_obj = RouterInfo_Serializer(routerInfo_list, many=True)

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "success"
            base_DTO_obj.massage = "get routeInfo"
            base_DTO_obj.data_list = routerInfo_serializer_obj.data

            routerInfo_list_Serializer_DTO_obj = RouterInfo_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(routerInfo_list_Serializer_DTO_obj.data, status=status.HTTP_200_OK)
        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "error"
            base_DTO_obj.massage = e 
            # base_DTO_obj.data_list = order_serializer.data

            routerInfo_list_Serializer_DTO_obj = RouterInfo_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(routerInfo_list_Serializer_DTO_obj.data, status=status.HTTP_200_OK)

        

            # return JsonResponse(order_serializer.data, safe=False)

    elif request.method == 'POST':


        try:
            routerInfo_data = JSONParser().parse(request)
            routerInfo_data['updated_by'] = request.user.username

            if routerInfo_data['project_code'] is None or routerInfo_data['project_code'].strip() == "" :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("ROUTE_INFO_PROJECTCODE_REQUIRED").data
                base_DTO_obj.data = None

                routerInfo_Serializer_DTO = RouterInfo_Serializer_DTO(base_DTO_obj)

                return JsonResponse(routerInfo_Serializer_DTO.data, status=status.HTTP_200_OK) 

            elif routerInfo_data['route_code'] is None or routerInfo_data['route_code'].strip() == "" :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("ROUTE_INFO_ROUTECODE_REQUIRED").data
                base_DTO_obj.data = None

                routerInfo_Serializer_DTO = RouterInfo_Serializer_DTO(base_DTO_obj)

                return JsonResponse(routerInfo_Serializer_DTO.data, status=status.HTTP_200_OK) 
            
            elif routerInfo_data['trip_no'] is None or routerInfo_data['trip_no'].strip() == "" :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("ROUTE_INFO_TRIPNO_REQUIRED").data
                base_DTO_obj.data = None

                routerInfo_Serializer_DTO = RouterInfo_Serializer_DTO(base_DTO_obj)

                return JsonResponse(routerInfo_Serializer_DTO.data, status=status.HTTP_200_OK) 
            
            elif routerInfo_data['province'] is None or routerInfo_data['province'].strip() == "" :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage =configMessage.configs.get("ROUTE_INFO_PROVINCE_REQUIRED").data
                base_DTO_obj.data = None

                routerInfo_Serializer_DTO = RouterInfo_Serializer_DTO(base_DTO_obj)

                return JsonResponse(routerInfo_Serializer_DTO.data, status=status.HTTP_200_OK)
        
            elif routerInfo_data['truck_license'] is None or routerInfo_data['truck_license'].strip() == "" :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("ROUTE_INFO_TRUCKLICENSE_REQUIRED").data
                base_DTO_obj.data = None

                routerInfo_Serializer_DTO = RouterInfo_Serializer_DTO(base_DTO_obj)

                return JsonResponse(routerInfo_Serializer_DTO.data, status=status.HTTP_200_OK)  
            
            elif routerInfo_data['driver_code'] is None or routerInfo_data['driver_code'].strip() == "" :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("ROUTE_INFO_DRIVERCODE_REQUIRED").data
                base_DTO_obj.data = None

                routerInfo_Serializer_DTO = RouterInfo_Serializer_DTO(base_DTO_obj)

                return JsonResponse(routerInfo_Serializer_DTO.data, status=status.HTTP_200_OK)

            else:  

                routerInfo_serializer_obj = RouterInfo_Serializer(data=routerInfo_data)
                if routerInfo_serializer_obj.is_valid():
                    
                    routerInfo_serializer_obj.save()
                    base_DTO_obj =  base_DTO()
                    base_DTO_obj.serviceStatus = "success"
                    base_DTO_obj.massage = configMessage.configs.get("ROUTE_INFO_ADD_MASSAGE_SUCCESSFUL").data
                    base_DTO_obj.data = routerInfo_serializer_obj.data

                    routerInfo_Serializer_DTO_reponse = RouterInfo_Serializer_DTO(base_DTO_obj)

                    return JsonResponse(routerInfo_Serializer_DTO_reponse.data, status=status.HTTP_200_OK) 
                

                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = routerInfo_serializer_obj.errors
                base_DTO_obj.data = None

                routerInfo_Serializer_DTO_reponse = RouterInfo_Serializer_DTO(base_DTO_obj)

                return JsonResponse(routerInfo_Serializer_DTO_reponse.data, status=status.HTTP_200_OK)

        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = e
            base_DTO_obj.data = None

            routerInfo_Serializer_DTO = RouterInfo_Serializer_DTO(base_DTO_obj)

        return JsonResponse(routerInfo_Serializer_DTO.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def search_route_info(request):

    if request.method == 'POST':

        try:
            customer_code_selected = request.data['customer_code_selected']
            project_code_selected = request.data['project_code_selected']
          
            route_code_selected = request.data['route_code_selected']
            trip_no_selected = request.data['trip_no_selected']

            query = "select * from master_data_routerinfo "

            joint_str = "" 
            where_str = " where 1 = 1  and master_data_routerinfo.is_active = true  "


            if customer_code_selected is not None:

                joint_str = joint_str + " INNER JOIN master_data_project "
                joint_str = joint_str + " ON UPPER(master_data_project.project_code) = UPPER(master_data_routerinfo.project_code) "
                joint_str = joint_str + " INNER JOIN master_data_customer "
                joint_str = joint_str + " ON UPPER(master_data_customer.customer_code) = UPPER(master_data_project.customer_code) "
                where_str = where_str + " and  UPPER(master_data_customer.customer_code) = '%s' " % customer_code_selected.upper()
                    
            if project_code_selected is not None:

                where_str = where_str + " and  UPPER(master_data_routerinfo.project_code) = '%s' " % project_code_selected.upper()


            if route_code_selected is not None:
                joint_str = joint_str + " INNER JOIN master_data_routermaster "
                joint_str = joint_str + " ON UPPER(master_data_routermaster.route_code) = UPPER(master_data_routerinfo.route_code) "
                where_str = where_str + " and  UPPER(master_data_routermaster.route_code) = '%s' " % route_code_selected.upper()
            
            if trip_no_selected is not None and route_code_selected is None:

                joint_str = joint_str + " INNER JOIN master_data_routermaster "
                joint_str = joint_str + " ON UPPER(master_data_routermaster.route_code) = UPPER(master_data_routerinfo.route_code) "
                where_str = where_str + " and  UPPER(master_data_routermaster.trip_no) = '%s' " % trip_no_selected.upper()

            if trip_no_selected is not None and route_code_selected is not None:

                where_str = where_str + " and  UPPER(master_data_routermaster.trip_no) = '%s' " % trip_no_selected.upper()

            query = query + joint_str + where_str + " Order By master_data_routerinfo.updated_date desc"
            print(query)
            routerInfo_list = RouterInfo.objects.raw(query)

            routerInfo_csv_list = []

            routerInfo_csv_list.insert(0, [
                "Project Code",
                "Route Code",
                "Trip No",
                "Truck License"
                "Province",
                "Driver",
                "Update by",
                "Update Date"
                ]
            )

            routeInfo_dto_list = []
            for routerInfo_obj in routerInfo_list:

                routeInfo_dto_obj =  RouteInfoDTO()
                routeInfo_dto_obj.id = routerInfo_obj.id
                routeInfo_dto_obj.project_code = routerInfo_obj.project_code
                # routeInfo_dto_obj.route_no = routerInfo_obj.route_no
                routeInfo_dto_obj.driver_code = routerInfo_obj.driver_code
                routeInfo_dto_obj.route_code = routerInfo_obj.route_code
                routeInfo_dto_obj.trip_no = routerInfo_obj.trip_no
                routeInfo_dto_obj.truck_license = routerInfo_obj.truck_license
                routeInfo_dto_obj.province = routerInfo_obj.province
                
                if routerInfo_obj.driver_code :
                    routeInfo_dto_obj.driver_name = Driver.objects.filter(driver_code=routerInfo_obj.driver_code)[0].name
                
                routeInfo_dto_obj.updated_by = routerInfo_obj.updated_by
                routeInfo_dto_obj.updated_date = routerInfo_obj.updated_date

            
                routeInfo_dto_list.append(routeInfo_dto_obj)

                routeInfo_row_list = (
                                routeInfo_dto_obj.project_code,
                                routeInfo_dto_obj.route_code,
                                routeInfo_dto_obj.trip_no,
                                routeInfo_dto_obj.truck_license,
                                routeInfo_dto_obj.province,
                                routeInfo_dto_obj.driver_name,
                                routeInfo_dto_obj.updated_by,
                                routeInfo_dto_obj.updated_date.strftime("%d/%m/%Y")
                                )

                routerInfo_csv_list.append(routeInfo_row_list)

            name_csv_str = "RouterInfoCSV" +datetime.now().strftime("%Y%m%d_%H%M%S")

            with open("media/" +  name_csv_str +'.csv', 'w', newline='',encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(routerInfo_csv_list)

            routeInfo_serializer = RouterInfo_Serializer(routeInfo_dto_list, many=True)

            
            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "success"
            base_DTO_obj.massage = "get part"
            base_DTO_obj.data_list = routeInfo_serializer.data
            base_DTO_obj.csv_name =  name_csv_str + '.csv'

            routerInfo_list_Serializer_DTO = RouterInfo_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(routerInfo_list_Serializer_DTO.data, safe=False)

        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = e
            base_DTO_obj.data = None

            routerInfo_list_Serializer_DTO = RouterInfo_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(routerInfo_list_Serializer_DTO.data, safe=False)

@api_view(['GET', 'POST', 'DELETE'])
def edited_routeInfo(request):

    if request.method == 'POST':

        try:

            routerInfo_data = JSONParser().parse(request)

            if routerInfo_data['province'] is None or routerInfo_data['province'].strip() == "" :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("ROUTE_INFO_PROVINCE_REQUIRED").data
                base_DTO_obj.data = None

                routerInfo_Serializer_DTO = RouterInfo_Serializer_DTO(base_DTO_obj)

                return JsonResponse(routerInfo_Serializer_DTO.data, status=status.HTTP_200_OK) 
            
            elif routerInfo_data['truck_license'] is None or routerInfo_data['truck_license'].strip() == "" :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error" 
                base_DTO_obj.massage = configMessage.configs.get("ROUTE_INFO_TRUCKLICENSE_REQUIRED").data
                base_DTO_obj.data = None

                routerInfo_Serializer_DTO = RouterInfo_Serializer_DTO(base_DTO_obj)

                return JsonResponse(routerInfo_Serializer_DTO.data, status=status.HTTP_200_OK)
            
            
            
            elif routerInfo_data['driver_code'] is None or routerInfo_data['driver_code'].strip() == "" :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("ROUTE_INFO_DRIVERCODE_REQUIRED").data
                base_DTO_obj.data = None

                routerInfo_Serializer_DTO = RouterInfo_Serializer_DTO(base_DTO_obj)

                return JsonResponse(routerInfo_Serializer_DTO.data, status=status.HTTP_200_OK)
            
            else : 

                routerInfo_obj = RouterInfo.objects.filter( id=routerInfo_data['id'])
                routerInfo_serializer_obj = RouterInfo_Serializer(routerInfo_obj[0],data=routerInfo_data)

                if routerInfo_serializer_obj.is_valid():

                    routerInfo_serializer_obj.save()
                    
                    base_DTO_obj =  base_DTO()
                    base_DTO_obj.serviceStatus = "success"
                    base_DTO_obj.massage = configMessage.configs.get("ROUTE_INFO_EDIT_MASSAGE_SUCCESSFUL").data
                    base_DTO_obj.routeInfo_list = RouterInfo.objects.all()

                    routerInfo_list_serializer_DTO_reponse = RouterInfo_list_Serializer_DTO(base_DTO_obj)

                    return JsonResponse(routerInfo_list_serializer_DTO_reponse.data, safe=False) 

        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = e
            base_DTO_obj.data = None

            routerInfo_Serializer_DTO_reponse = RouterInfo_Serializer_DTO(base_DTO_obj)

            return JsonResponse(routerInfo_Serializer_DTO_reponse.data, safe=False)


@api_view(['GET', 'POST', 'DELETE'])
def deleted_routeInfo(request):

    if request.method == 'POST':

        try:

            routeInfo_data = JSONParser().parse(request)
            print(routeInfo_data)
            routerInfo_list = RouterInfo.objects.filter(id__in=routeInfo_data)
            routerInfo_list.update(is_active = False)

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "success"
            base_DTO_obj.massage = configMessage.configs.get("ROUTE_INFO_DELETE_MASSAGE_SUCCESSFUL").data
            base_DTO_obj.data_list = RouterInfo.objects.filter(is_active=True)

            routerInfo_list_serializer_DTO_reponse = RouterInfo_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(routerInfo_list_serializer_DTO_reponse.data, safe=False) 
            
        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = e
            base_DTO_obj.data = None

            routerInfo_Serializer_DTO_reponse = RouterInfo_Serializer_DTO(base_DTO_obj)

            return JsonResponse(routerInfo_Serializer_DTO_reponse.data, safe=False)


@api_view(['GET', 'POST', 'DELETE'])
def calendarMaster_list(request):
    
    if request.method == 'GET':
        try:
            calendarMaster_list = CalendarMaster.objects.filter(is_active=True)

            serializer = serializerMapping.mapping_serializer_list(
                CalendarMaster_list_Serializer_DTO,
                calendarMaster_list,
                "success", 
                "",
                "",
                None,
                None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:

            serializer = serializerMapping.mapping_serializer_list(
                    Customer_list_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None )

            return Response(serializer.data, status=status.HTTP_200_OK)

       
 

@api_view(['POST'])
def search_calendarMaster(request):

    if request.method == 'POST':

        try:
            customer_code = request.data['customer_code_selected']
            project_code = request.data['project_code_selected']
            plant_code = request.data['plant_code_selected']
            working_day = request.data['working_day_selected']

            calendarMasterService = CalendarMasterService()
            calendarMaster_list =  calendarMasterService.search_calendarMaster(customer_code,project_code,plant_code,working_day)

            name_csv_str = "CalendarMasterCSV_" +datetime.now().strftime("%Y%m%d_%H%M%S")
            CSV_file_management_obj = CSVFileManagement(name_csv_str,"media/",'',',')
            CSV_file_management_obj.covert_to_header([
                "Plant",
                "Day",
                "Date",
                "Working Day",
                "Remark",
                "Update by",
                "Update Date"])
            calendarMaster_CSV_list  = CalendarMasterHelper.covert_data_list_to_CSV_list(calendarMaster_list)
            CSV_file_management_obj.covert_to_CSV_data_list(calendarMaster_CSV_list)
            return_name_CSV_str = CSV_file_management_obj.genearete_CSV_file()

            serializer_list =  CalendarMasterHelper.covert_data_list_to_serializer_list(calendarMaster_list)

            serializer = serializerMapping.mapping_serializer_list(
                CalendarMaster_list_Serializer_DTO,
                serializer_list,
                "success", 
                "",
                name_csv_str + '.csv',
                None,
                None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:

            serializer = serializerMapping.mapping_serializer_list(
                    CalendarMaster_list_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)




@api_view(['GET', 'POST', 'DELETE'])
def deleted_calendarMaster(request):

    if request.method == 'POST':

        try:

            calendarMaster_data = JSONParser().parse(request)
            calendarMaster_list = CalendarMaster.objects.filter(id__in=calendarMaster_data)
            calendarMaster_list.update(is_active = False)

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "success"
            base_DTO_obj.massage = configMessage.configs.get("CALENDAR_MASTER_DELETE_MASSAGE_SUCCESSFUL").data
            base_DTO_obj.data = None

            calendarMaster_serializer_DTO = CalendarMaster_Serializer_DTO(base_DTO_obj)

            return JsonResponse(calendarMaster_serializer_DTO.data, safe=False) 
            

        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = e
            base_DTO_obj.data = None

            calendarMaster_Serializer_DTO_reponse = CalendarMaster_Serializer_DTO(base_DTO_obj)

            return JsonResponse(calendarMaster_Serializer_DTO_reponse.data, safe=False)


@api_view(['GET', 'POST', 'DELETE'])
def add_part_master(request):

    if request.method == 'GET':

        with open("media/" + "add_partMaster.csv", newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar=',')
            for row in spamreader:

                add_part =  Part()
                add_part.project_code = row[0]
                add_part.status = 2
                add_part.supplier_code = row[1]
                add_part.part_number = row[2]
                add_part.part_name = row[3]
                add_part.package_no = row[4]
                add_part.package_volume = 0.00
                add_part.package_weight = 0.00
                add_part.is_active = True
                add_part.save()
        return JsonResponse("test", safe=False)


@api_view(['GET', 'POST', 'DELETE'])
def add_packages_master(request):

    if request.method == 'GET':

        with open("media/" + "add_packageMaster.csv", newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar=',')
            for row in spamreader:



                add_package =  Package()
                add_package.station_code = row[0]
                add_package.package_code = row[1]
                add_package.package_no = row[2]
                add_package.width = Decimal(row[3])
                add_package.length = Decimal(row[4])
                add_package.height = Decimal(row[5])
                add_package.weight = Decimal(row[6])
                add_package.image_url = ""
                add_package.is_active = True
                add_package.save()
        return JsonResponse("test", safe=False)


