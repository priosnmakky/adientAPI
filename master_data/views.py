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
from app.helper.truck_helper.TruckHelper import TruckHelper
from app.services.truck_service.TruckService import TruckService
from app.helper.driver_helper.DriverHelper import DriverHelper
from app.services.driver_service.DriverService import DriverService
from app.helper.routerMaster_helper.RouterMasterHelper import RouterMasterHelper
from app.services.routerMaster_service.RouterMasterService import RouterMasterService
from app.helper.routerInfo_helper.RouterInfoHelper import RouterInfoHelper
from app.services.routerInfo_service.RouterInfoService import RouterInfoService
import json
from app.helper.config.ConfigPart import ConfigPart


configMessage = ConfigMessage()
configPart = ConfigPart()
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

            router_list_Serializer_DTO_obj = Router_master_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(router_list_Serializer_DTO_obj.data, status=status.HTTP_200_OK)

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

            station_list_Serializer_DTO_obj = Station_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(station_list_Serializer_DTO_obj.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'DELETE'])
def plant_list(request):
    

    if request.method == 'GET':
        try:
            station_list = Station.objects.filter(station_type = 'PLANT',is_active=True)
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
            base_DTO_obj.massage = "error"

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

            CSV_part_str = FileManagement.validate_folder(configPart.configs.get("PROJECT_MASTERDATA_PART").data)
            CSV_part_generete_str = 'media/' + CSV_part_str + "/"

            projectService = ProjectService()
            project_list =  projectService.search_project(customer_code)
            
            name_csv_str = "ProjectMasterCSV" +datetime.now().strftime("%Y%m%d_%H%M%S")
            CSV_file_management_obj = CSVFileManagement(name_csv_str,CSV_part_generete_str,'',',')
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
                CSV_part_str + "/" + name_csv_str + '.csv',
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

            CSV_part_str = FileManagement.validate_folder(configPart.configs.get("STATION_MASTERDATA_PART").data)
            CSV_part_generete_str = 'media/' + CSV_part_str + "/"

            customerService = CustomerService()
            customer_list =  customerService.search_customer(customer_code,project_code,stationCode_code)

            name_csv_str = "StationMasterCSV" +datetime.now().strftime("%Y%m%d_%H%M%S")
            CSV_file_management_obj = CSVFileManagement(name_csv_str,CSV_part_generete_str,'',',')
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
                CSV_part_str + "/" + name_csv_str + '.csv',
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

                    print()

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
                    
                    print()
                    
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

            CSV_part_str = FileManagement.validate_folder(configPart.configs.get("PACKAGES_MASTERDATA_PART").data)
            CSV_part_generete_str = 'media/' + CSV_part_str + "/"

            packageService = PackageService()
            package_list = packageService.search_package(customer_code,project_code,supplier_code,package_code,package_no)
     
            name_csv_str = "PackageMasterCSV_" +datetime.now().strftime("%Y%m%d_%H%M%S")
            CSV_file_management_obj = CSVFileManagement(name_csv_str,CSV_part_generete_str,'',',')
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
                CSV_part_str + "/" + name_csv_str + '.csv',
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
            serializer = serializerMapping.mapping_serializer_list(
                Truck_list_Serializer_DTO,
                truck_list,
                "success", 
                "",
                "",
                None,
                None )
            
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:

            serializer = serializerMapping.mapping_serializer_list(
                    Truck_list_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None )

            return Response(serializer.data, status=status.HTTP_200_OK)
        
    elif request.method == 'POST':
        
        try:
            truck_data = JSONParser().parse(request)
            truck_serializer_obj = Truck_Serializer(data=truck_data)

            if truck_serializer_obj.is_valid():
                
                truck_serializer_obj.save()
                truck_obj =  truck_serializer_obj.save(updated_by=request.user.username)

                serializer = serializerMapping.mapping_serializer_obj(
                    Truck_Serializer_DTO,
                    truck_obj,
                    "success", 
                    configMessage.configs.get("PART_MASTER_ADD_MASSAGE_SUCCESSFUL").data,
                    "",
                    None,
                    None )
            
            else : 

                serializer = serializerMapping.mapping_serializer_obj(
                    Truck_Serializer_DTO,
                    None,
                    "Error",
                    ErrorHelper.get_error_massage(truck_serializer_obj.errors),
                    None,
                    None,
                    None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:

            serializer = serializerMapping.mapping_serializer_obj(
                Truck_Serializer_DTO,
                None,
                "Error",
                e,
                None,
                None,
                None )
                
            return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'DELETE'])
def deleted_truck(request):

    if request.method == 'POST':

        try:

            truck_data = JSONParser().parse(request)
            truck_list = Truck.objects.filter(truck_license__in=truck_data)
            truck_list.update(is_active = False)

            serializer = serializerMapping.mapping_serializer_list(
                Truck_list_Serializer_DTO,
                truck_list,
                "success", 
                configMessage.configs.get("TRUCK_MASTER_DELETE_MASSAGE_SUCCESSFUL").data,
                "",
                None,
                None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:

            serializer = serializerMapping.mapping_serializer_list(
                    Truck_list_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'DELETE'])
def edited_truck(request):

    if request.method == 'POST':

        try:

            truck_data = JSONParser().parse(request)

            truck_obj = Truck.objects.filter( truck_license = truck_data["truck_license"] )[0]
            truck_serializer_obj = Truck_Serializer(truck_obj,data=truck_data)

            if truck_serializer_obj.is_valid():

                truck_serializer_obj.save()

                serializer = serializerMapping.mapping_serializer_obj(
                    Truck_Serializer_DTO,
                    truck_obj,
                    "success", 
                    configMessage.configs.get("TRUCK_MASTER_EDIT_MASSAGE_SUCCESSFUL").data ,
                    "",
                    None,
                    None 
                    )

            else :

                serializer = serializerMapping.mapping_serializer_obj(
                    Truck_Serializer_DTO,
                    None,
                    "Error",
                    ErrorHelper.get_error_massage(truck_serializer_obj.errors),
                    None,
                    None,
                    None )
                    
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:

            serializer = serializerMapping.mapping_serializer_obj(
                    Truck_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def search_truck(request):

    if request.method == 'POST':

        try:

            truck_data_obj = JSONParser().parse(request)

            truck_licese = truck_data_obj['truck_licese']
            province = truck_data_obj['truck_province']
            truck_type = truck_data_obj['truck_type']
            truck_fuel = truck_data_obj['truck_fuel']

            CSV_part_str = FileManagement.validate_folder(configPart.configs.get("TRUCK_MASTERDATA_PART").data)
            CSV_part_generete_str = 'media/' + CSV_part_str + "/"

            truckService = TruckService()
            truck_list =  truckService.search_truck(truck_licese,province,truck_type,truck_fuel)

            name_csv_str = "TruckCSV_" +datetime.now().strftime("%Y%m%d_%H%M%S")
            CSV_file_management_obj = CSVFileManagement(name_csv_str,CSV_part_generete_str,'',',')
            CSV_file_management_obj.covert_to_header([
                "Truck License",
                "Province",
                "Truck Type",
                "Fuel Type",
                "Max Speed",
                "Max Volume",
                "Max Weight",
                "Remark",
                "Update By",
                "Update Date",])

            truck_CSV_list = TruckHelper.covert_data_list_to_CSV_list(truck_list)
            CSV_file_management_obj.covert_to_CSV_data_list(truck_CSV_list)
            return_name_CSV_str = CSV_file_management_obj.genearete_CSV_file()

            serializer_list =  TruckHelper.covert_data_list_to_serializer_list(truck_list)

            serializer = serializerMapping.mapping_serializer_list(
                    Truck_list_Serializer_DTO,
                    serializer_list,
                    "success", 
                    "",
                    CSV_part_str + "/" + name_csv_str + '.csv',
                    None,
                    None
                )
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:

            serializer = serializerMapping.mapping_serializer_list(
                    Truck_list_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None 
                )

            return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'DELETE'])
def driver_list(request):
    
    if request.method == 'GET':
        try:
            
            driver_list = Driver.objects.filter(is_active=True)

            serializer = serializerMapping.mapping_serializer_list(
                Driver_list_Serializer_DTO,
                driver_list,
                "success", 
                "",
                "",
                None,
                None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:

            serializer = serializerMapping.mapping_serializer_list(
                    Driver_list_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None )

            return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':

        try:

            driver_data = JSONParser().parse(request)
            driver_serializer_obj = Driver_Serializer(data=driver_data)

            if driver_serializer_obj.is_valid():

                driver_serializer_obj.save()
                driver_obj =  driver_serializer_obj.save(updated_by=request.user.username)

                serializer = serializerMapping.mapping_serializer_obj(
                    Driver_Serializer_DTO,
                    driver_obj,
                    "success", 
                    configMessage.configs.get("DRIVER_MASTER_ADD_MASSAGE_SUCCESSFUL").data,
                    "",
                    None,
                    None )
            
            else : 

                serializer = serializerMapping.mapping_serializer_obj(
                    Driver_Serializer_DTO,
                    None,
                    "Error",
                    ErrorHelper.get_error_massage(driver_serializer_obj.errors),
                    None,
                    None,
                    None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:

            serializer = serializerMapping.mapping_serializer_obj(
                Driver_Serializer_DTO,
                None,
                "Error",
                e,
                None,
                None,
                None )
                
            return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST', 'DELETE'])
def deleted_driver(request):

    if request.method == 'POST':

        try:

            driver_data = JSONParser().parse(request)
            driver_list = Driver.objects.filter(driver_code__in=driver_data)
            
            driver_list.update(is_active = False)

            serializer = serializerMapping.mapping_serializer_list(
                Driver_list_Serializer_DTO,
                driver_list,
                "success", 
                configMessage.configs.get("DRIVER_MASTER_DELETE_MASSAGE_SUCCESSFUL").data,
                "",
                None,
                None )
            
            return Response(serializer.data, status=status.HTTP_200_OK) 
        
        except Exception as e:

            serializer = serializerMapping.mapping_serializer_list(
                    Driver_list_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'DELETE'])
def edited_driver(request):

    if request.method == 'POST':

        try:

            driver_data = JSONParser().parse(request)
            driver_obj = Driver.objects.filter( driver_code = driver_data["driver_code"] )[0]
            driver_serializer_obj = Driver_Serializer(driver_obj,data=driver_data)

            if driver_serializer_obj.is_valid():

                driver_serializer_obj.save()

                serializer = serializerMapping.mapping_serializer_obj(
                    Driver_Serializer_DTO,
                    driver_obj,
                    "success", 
                    configMessage.configs.get("DRIVER_MASTER_EDIT_MASSAGE_SUCCESSFUL").data,
                    "",
                    None,
                    None 
                    )
            
            else :

                serializer = serializerMapping.mapping_serializer_obj(
                    Driver_Serializer_DTO,
                    None,
                    "Error",
                    ErrorHelper.get_error_massage(driver_serializer_obj.errors),
                    None,
                    None,
                    None )
                    
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:    

            serializer = serializerMapping.mapping_serializer_obj(
                    Driver_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)
    

@api_view(['POST'])
def search_driver(request):

    if request.method == 'POST':

        try:

            driver_data_obj = JSONParser().parse(request)
            driver_code = driver_data_obj['driver_code']
            driver_name = driver_data_obj['driver_name']

            CSV_part_str = FileManagement.validate_folder(configPart.configs.get("DRIVER_MASTERDATA_PART").data)
            CSV_part_generete_str = 'media/' + CSV_part_str + "/"

            driverService  = DriverService()
            driver_list  = driverService.search_driver(driver_code,driver_name)

            name_csv_str = "DriverMasterCSV" +datetime.now().strftime("%Y%m%d_%H%M%S")
            CSV_file_management_obj = CSVFileManagement(name_csv_str,CSV_part_generete_str,'',',')
            CSV_file_management_obj.covert_to_header([
                "Driver Code",
                "Driver Name",
                "Driver Tel",
                "Remark",
                "Updated By",
                "Updated Date"])

            driver_CSV_list = DriverHelper.covert_data_list_to_CSV_list(driver_list)
            CSV_file_management_obj.covert_to_CSV_data_list(driver_CSV_list)
            return_name_CSV_str = CSV_file_management_obj.genearete_CSV_file()

            serializer_list =  DriverHelper.covert_data_list_to_serializer_list(driver_list)

            serializer = serializerMapping.mapping_serializer_list(
                    Driver_list_Serializer_DTO,
                    serializer_list,
                    "success", 
                    "",
                    CSV_part_str + "/" + name_csv_str + '.csv',
                    None,
                    None
                )
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:

            serializer = serializerMapping.mapping_serializer_list(
                    Driver_list_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None 
                )
            
            return Response(serializer.data, status=status.HTTP_200_OK)

@api_view([ 'POST'])      
def search_route_master(request):

    if request.method == 'POST':

        try:
            customer_code = request.data['customer_code_selected']
            project_code = request.data['project_code_selected']
            supplier_code = request.data['supplier_code_selected']
            plant_code = request.data['plant_code_selected']
            route_code = request.data['route_code_selected']
            route_trip = request.data['trip_no_selected']

            CSV_part_str = FileManagement.validate_folder(configPart.configs.get("ROUTEINFO_MASTERDATA_PART").data)
            CSV_part_generete_str = 'media/' + CSV_part_str + "/"

            routerMasterService = RouterMasterService()
            routerMaster_list =  routerMasterService.search_routerMaster(customer_code,project_code,supplier_code,plant_code,route_code,route_trip)

            name_csv_str = "RouterMasterCSV_" +datetime.now().strftime("%Y%m%d_%H%M%S")
            CSV_file_management_obj = CSVFileManagement(name_csv_str,CSV_part_generete_str,'',',')
            CSV_file_management_obj.covert_to_header([
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
                "Update Date"])

            routerMaster_CSV_list = RouterMasterHelper.covert_data_list_to_CSV_list(routerMaster_list)
            CSV_file_management_obj.covert_to_CSV_data_list(routerMaster_CSV_list)
            return_name_CSV_str = CSV_file_management_obj.genearete_CSV_file()

            serializer_list =  RouterMasterHelper.covert_data_list_to_serializer_list(routerMaster_list)

            serializer = serializerMapping.mapping_serializer_list(
                    RouterMaster_list_Serializer_DTO,
                    serializer_list,
                    "success", 
                    "",
                    CSV_part_str + "/" + name_csv_str + '.csv',
                    None,
                    None
                )


            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:

            serializer = serializerMapping.mapping_serializer_list(
                    RouterMaster_list_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None 
                )
            
            return Response(serializer.data, status=status.HTTP_200_OK)
  

@api_view(['GET', 'POST', 'DELETE'])
def routeMaster_list(request):
    
    if request.method == 'GET':
        try:

            routerMaster_list = RouterMaster.objects.filter(is_active=True)

            serializer = serializerMapping.mapping_serializer_list(
                RouterMaster_list_Serializer_DTO,
                routerMaster_list,
                "success", 
                "",
                "",
                None,
                None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:

            serializer = serializerMapping.mapping_serializer_list(
                    RouterMaster_list_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None )

            return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':

        try:

            routerMaster_data = JSONParser().parse(request)
            routerMaster_serializer_obj = RouterMaster_Serializer(data=routerMaster_data)

            if routerMaster_serializer_obj.is_valid():

                routerMaster_serializer_obj.save()
                routerMaster_obj =  routerMaster_serializer_obj.save(updated_by=request.user.username)

                serializer = serializerMapping.mapping_serializer_obj(
                    RouterMaster_Serializer_DTO,
                    routerMaster_obj,
                    "success", 
                    configMessage.configs.get("ROUTE_MASTER_ADD_MASSAGE_SUCCESSFUL").data,
                    "",
                    None,
                    None )
            
            else : 
                
                serializer = serializerMapping.mapping_serializer_obj(
                    RouterMaster_Serializer_DTO,
                    None,
                    "Error",
                    ErrorHelper.get_error_massage(routerMaster_serializer_obj.errors),
                    None,
                    None,
                    None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:

            serializer = serializerMapping.mapping_serializer_obj(
                RouterMaster_Serializer_DTO,
                None,
                "Error",
                e,
                None,
                None,
                None )
                
            return Response(serializer.data, status=status.HTTP_200_OK)
         
     

@api_view(['POST'])
def upload_route_master(request):
    
    if request.method == 'POST':

        try:
            
            file_serializer = File_Serializer(data=request.data)
        
            if file_serializer.is_valid():

                file_part_str = FileManagement.validate_folder(configPart.configs.get("ROUTEMASTER_UPDATE_MASTERDATA_PART").data)
                
                upload_route_master_file = request.FILES['file']
                fs = FileSystemStorage(location="media/"+ file_part_str+"/") #defaults to   MEDIA_ROOT  
                file_name_str = fs.save(upload_route_master_file.name, upload_route_master_file)

                validateWarning_list = []
                validate_error_list_serializer= []

                with open("media/" + file_part_str+"/"+file_name_str, newline='') as csvfile:
                    routerMaster_list = csv.reader(csvfile, delimiter=',', quotechar='|')
            
                    routerMasterHelper = RouterMasterHelper()
        
                    routerMaster_list = routerMasterHelper.validate_routeMaster(routerMaster_list)

                    if len(routerMasterHelper.validateError_list) <= 0: 

                        routerMasterService =  RouterMasterService()
                        routerMasterService.update_routerMaster(routerMaster_list)

                    validate_error_list_serializer = validate_error_serializer(routerMasterHelper.validateError_list, many=True)   

                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "success"
                base_DTO_obj.massage = configMessage.configs.get("ROUTE_MASTER_EDIT_MASSAGE_SUCCESSFUL").data
                base_DTO_obj.data_list = None
                base_DTO_obj.validate_error_list =  validate_error_list_serializer.data

                serializer = RouterMaster_list_Serializer_DTO(base_DTO_obj)
                
                return Response(serializer.data, status=status.HTTP_200_OK)
                
            else :

                serializer = serializerMapping.mapping_serializer_obj(
                    RouterMaster_Serializer_DTO,
                    None,
                    "Error",
                    ErrorHelper.get_error_massage(file_serializer.errors),
                    None,
                    None,
                    None )
                
                return Response(serializer.data, status=status.HTTP_200_OK)
                

        except Exception as e:

            serializer = serializerMapping.mapping_serializer_obj(
                    RouterMaster_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'DELETE'])
def deleted_routeMaster(request):

    if request.method == 'POST':

        try:

            routeMaster_data = JSONParser().parse(request)
            routeMaster_list = RouterMaster.objects.filter(route_no__in=routeMaster_data)
            routeMaster_list.update(is_active = False)

            serializer = serializerMapping.mapping_serializer_list(
                RouterMaster_list_Serializer_DTO,
                routeMaster_list,
                "success", 
                configMessage.configs.get("ROUTE_MASTER_DELETE_MASSAGE_SUCCESSFUL").data,
                "",
                None,
                None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:

            serializer = serializerMapping.mapping_serializer_list(
                    RouterMaster_list_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        

@api_view(['GET', 'POST', 'DELETE'])
def routeInfo_list(request):
    
    if request.method == 'GET':

        try:

            routerInfo_list = RouterInfo.objects.filter(is_active=True)

            serializer = serializerMapping.mapping_serializer_list(
                RouterInfo_list_Serializer_DTO,
                routerInfo_list,
                "success", 
                "",
                "",
                None,
                None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:

            serializer = serializerMapping.mapping_serializer_list(
                    RouterInfo_list_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None )

            return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':

        try:

            routerInfo_data = JSONParser().parse(request)
            routerInfo_serializer_obj = RouterInfo_Serializer(data=routerInfo_data)

            if routerInfo_serializer_obj.is_valid():
            
                routerInfo_serializer_obj.save()
                routerInfo_obj =  routerInfo_serializer_obj.save(updated_by=request.user.username)

                serializer = serializerMapping.mapping_serializer_obj(
                    RouterInfo_Serializer_DTO,
                    routerInfo_obj,
                    "success", 
                    configMessage.configs.get("ROUTE_INFO_ADD_MASSAGE_SUCCESSFUL").data,
                    "",
                    None,
                    None )
                
            else : 

                serializer = serializerMapping.mapping_serializer_obj(
                    RouterInfo_Serializer_DTO,
                    None,
                    "Error",
                    ErrorHelper.get_error_massage(routerInfo_serializer_obj.errors),
                    None,
                    None,
                    None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:

            serializer = serializerMapping.mapping_serializer_obj(
                RouterInfo_Serializer_DTO,
                None,
                "Error",
                e,
                None,
                None,
                None )
                
            return Response(serializer.data, status=status.HTTP_200_OK)
         

@api_view(['POST'])
def search_route_info(request):

    if request.method == 'POST':

        try:

            customer_code = request.data['customer_code_selected']
            project_code = request.data['project_code_selected']
            route_code = request.data['route_code_selected']
            route_trip = request.data['trip_no_selected']

            CSV_part_str = FileManagement.validate_folder(configPart.configs.get("ROUTEINFO_MASTERDATA_PART").data)
            CSV_part_generete_str = 'media/' + CSV_part_str + "/"

            routerInfoService = RouterInfoService()
            routerInfo_list = routerInfoService.search_RouterInfo(customer_code,project_code,route_code,route_trip)

            name_csv_str = "RouterInfoCSV_" +datetime.now().strftime("%Y%m%d_%H%M%S")
            CSV_file_management_obj = CSVFileManagement(name_csv_str,CSV_part_generete_str,'',',')
            CSV_file_management_obj.covert_to_header([
                "Project Code",
                "Route Code",
                "Trip No",
                "Province",
                "Truck License",
                "Driver",
                "Update by",
                "Update Date"])

            routerInfo_CSV_list = RouterInfoHelper.covert_data_list_to_CSV_list(routerInfo_list)
            CSV_file_management_obj.covert_to_CSV_data_list(routerInfo_CSV_list)
            return_name_CSV_str = CSV_file_management_obj.genearete_CSV_file()

            serializer_list =  RouterInfoHelper.covert_data_list_to_serializer_list(routerInfo_list)

            serializer = serializerMapping.mapping_serializer_list(
                    RouterInfo_list_Serializer_DTO,
                    serializer_list,
                    "success", 
                    "",
                    CSV_part_str + "/" + name_csv_str + '.csv',
                    None,
                    None
                )
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:

            serializer = serializerMapping.mapping_serializer_list(
                    RouterInfo_list_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)

    
@api_view(['GET', 'POST', 'DELETE'])
def edited_routeInfo(request):

    if request.method == 'POST':

        try:

            routerInfo_data = JSONParser().parse(request)
            routerInfo_obj = RouterInfo.objects.filter( id=routerInfo_data['id'])[0]
            routerInfo_serializer_obj = RouterInfo_Serializer(routerInfo_obj,data=routerInfo_data)

            if routerInfo_serializer_obj.is_valid():

                routerInfo_serializer_obj.save()

                serializer = serializerMapping.mapping_serializer_obj(
                    RouterInfo_Serializer_DTO,
                    routerInfo_obj,
                    "success", 
                    configMessage.configs.get("ROUTE_INFO_EDIT_MASSAGE_SUCCESSFUL").data,
                    "",
                    None,
                    None 
                    )

            else :

                serializer = serializerMapping.mapping_serializer_obj(
                    RouterInfo_Serializer_DTO,
                    None,
                    "Error",
                    ErrorHelper.get_error_massage(routerInfo_serializer_obj.errors),
                    None,
                    None,
                    None )
                    
            
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:

            serializer = serializerMapping.mapping_serializer_obj(
                    RouterInfo_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'DELETE'])
def deleted_routeInfo(request):

    if request.method == 'POST':

        try:

            routeInfo_data = JSONParser().parse(request)
            routerInfo_list = RouterInfo.objects.filter(id__in=routeInfo_data)
            routerInfo_list.update(is_active = False)

            serializer = serializerMapping.mapping_serializer_list(
                RouterInfo_list_Serializer_DTO,
                routerInfo_list,
                "success", 
                configMessage.configs.get("ROUTE_INFO_DELETE_MASSAGE_SUCCESSFUL").data,
                "",
                None,
                None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:

            serializer = serializerMapping.mapping_serializer_list(
                    RouterInfo_list_Serializer_DTO,
                    None,
                    "Error",
                    e,
                    None,
                    None,
                    None )
            
            return Response(serializer.data, status=status.HTTP_200_OK)
      
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

            CSV_part_str = FileManagement.validate_folder(configPart.configs.get("CALENDAR_MASTERDATA_PART").data)
            CSV_part_generete_str = 'media/' + CSV_part_str + "/"

            calendarMasterService = CalendarMasterService()
            calendarMaster_list =  calendarMasterService.search_calendarMaster(customer_code,project_code,plant_code,working_day)

            name_csv_str = "CalendarMasterCSV_" +datetime.now().strftime("%Y%m%d_%H%M%S")
            CSV_file_management_obj = CSVFileManagement(name_csv_str,CSV_part_generete_str,'',',')
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
                CSV_part_str + "/" + name_csv_str + '.csv',
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



