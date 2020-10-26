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
from model_DTO.marter_data.customer_DTO import Customer_DTO
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

configMessage = ConfigMessage()


@api_view(['GET', 'POST', 'DELETE'])
def part_list(request):
    
    if request.method == 'GET':
        try:
            part_list = Part.objects.filter(is_active = True)
            order_serializer = Part_Serializer(part_list, many=True)

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "success"
            base_DTO_obj.massage = "get part"
            base_DTO_obj.data_list = order_serializer.data

            part_list_Serializer_DTO_obj = Part_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(part_list_Serializer_DTO_obj.data, status=status.HTTP_200_OK)
        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "error"
            base_DTO_obj.massage = "error"
            # base_DTO_obj.data_list = order_serializer.data

            part_list_Serializer_DTO_obj = Part_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(part_list_Serializer_DTO_obj.data, status=status.HTTP_200_OK)

        

            # return JsonResponse(order_serializer.data, safe=False)

    elif request.method == 'POST':


        try:
            part_data = JSONParser().parse(request)

            base_DTO_obj =  base_DTO()

            if part_data['project_code'] is None or part_data['project_code'].strip() == "" :

                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("PART_MASTER_PROJECTCODE_REQUIRED").data
                base_DTO_obj.data_list = None

                part_Serializer_DTO = Part_Serializer_DTO(base_DTO_obj)

                return JsonResponse(part_Serializer_DTO.data, safe=False) 

                    
            elif part_data['status'] is None or part_data['status'] == "" :

                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("PART_MASTER_STATUS_REQUIRED").data
                base_DTO_obj.data_list = None

                part_Serializer_DTO = Part_Serializer_DTO(base_DTO_obj)

                return JsonResponse(part_Serializer_DTO.data, safe=False) 

            
            elif part_data['supplier_code'] is None or part_data['supplier_code'].strip() == "" :

                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("PART_MASTER_SUPPLIERCODE_REQUIRED").data
                base_DTO_obj.data_list = None

                part_Serializer_DTO = Part_Serializer_DTO(base_DTO_obj)

                return JsonResponse(part_Serializer_DTO.data, safe=False) 

            elif part_data['part_number'] is None or part_data['part_number'].strip() == "" :

                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("PART_MASTER_PARTNUMBER_REQUIRED").data
                base_DTO_obj.data_list = None

                part_Serializer_DTO = Part_Serializer_DTO(base_DTO_obj)

                return JsonResponse(part_Serializer_DTO.data, safe=False) 

            elif part_data['part_name'] is None or part_data['part_name'].strip() == "" :

                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("PART_MASTER_PARTNAME_REQUIRED").data
                base_DTO_obj.data_list = None

                part_Serializer_DTO = Part_Serializer_DTO(base_DTO_obj)

                return JsonResponse(part_Serializer_DTO.data, safe=False) 

            elif part_data['package_no'] is None or part_data['package_no'].strip() == "" :

                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("PART_MASTER_PACKAGENO_REQUIRED").data
                base_DTO_obj.data_list = None

                part_Serializer_DTO = Part_Serializer_DTO(base_DTO_obj)

                return JsonResponse(part_Serializer_DTO.data, safe=False) 

            
            elif part_data['package_volume'] is None or part_data['package_volume'] == "" :

                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("PART_MASTER_PACKAGEVOLUME_REQUIRED").data
                base_DTO_obj.data_list = None

                part_Serializer_DTO = Part_Serializer_DTO(base_DTO_obj)

                return JsonResponse(part_Serializer_DTO.data, safe=False) 
            
            elif part_data['package_weight'] is None or part_data['package_weight'] == "" :

                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("PART_MASTER_PACKAGEWEIGHT_REQUIRED").data
                base_DTO_obj.data_list = None

                part_Serializer_DTO = Part_Serializer_DTO(base_DTO_obj)

                return JsonResponse(part_Serializer_DTO.data, safe=False) 

            else : 

                part_list = Part.objects.filter(part_number = part_data['part_number'])
                
            
                if len(part_list):

                    if part_list[0].is_active == True :

                        base_DTO_obj =  base_DTO()
                        base_DTO_obj.serviceStatus = "Error"
                        base_DTO_obj.massage = "Part Number duplicate"
                        base_DTO_obj.data = None

                        part_Serializer_DTO_reponse = Part_Serializer_DTO(base_DTO_obj)

                        return JsonResponse(part_Serializer_DTO_reponse.data, status=status.HTTP_200_OK)
                    
                    else : 

                        part_list.update(
                            part_name=part_data['part_name'],
                            package_no=part_data['package_no'],
                            package_volume=part_data['package_volume'],
                            package_weight=part_data['package_weight'],
                            is_active= True
                        )

                        base_DTO_obj =  base_DTO()
                        base_DTO_obj.serviceStatus = "success"
                        base_DTO_obj.massage = configMessage.configs.get("PART_MASTER_ADD_MASSAGE_SUCCESSFUL").data
                        base_DTO_obj.data = None

                        part_Serializer_DTO_reponse = Part_Serializer_DTO(base_DTO_obj)

                        return JsonResponse(part_Serializer_DTO_reponse.data, status=status.HTTP_201_CREATED) 
                        
                        
                else :

                    part_serializer_obj = Part_Serializer(data=part_data)

                    if part_serializer_obj.is_valid():

                        part_serializer_obj.save()

                        base_DTO_obj =  base_DTO()
                        base_DTO_obj.serviceStatus = "success"
                        base_DTO_obj.massage = configMessage.configs.get("PART_MASTER_ADD_MASSAGE_SUCCESSFUL").data
                        base_DTO_obj.data = part_serializer_obj.data

                        part_Serializer_DTO = Part_Serializer_DTO(base_DTO_obj)

                        return JsonResponse(part_Serializer_DTO.data, status=status.HTTP_201_CREATED) 

                    else :

                        base_DTO_obj =  base_DTO()
                        base_DTO_obj.serviceStatus = "Error"
                        base_DTO_obj.massage = part_serializer_obj.errors
                        base_DTO_obj.data = part_serializer_obj.data

                        part_list_Serializer_DTO = Part_list_Serializer_DTO(base_DTO_obj)

                        return JsonResponse(part_list_Serializer_DTO.data, status=status.HTTP_201_CREATED)

        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = e

            part_Serializer_DTO_reponse = Part_Serializer_DTO(base_DTO_obj)

        return JsonResponse(part_Serializer_DTO_reponse.data, status=status.HTTP_200_OK)

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
                    
            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "success"
            base_DTO_obj.massage = configMessage.configs.get("PART_MASTER_COMFIRM_MASSAGE_SUCCESSFUL").data
            base_DTO_obj.data_list = Part.objects.all()

            part_list_serializer_DTO_reponse = Part_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(part_list_serializer_DTO_reponse.data, safe=False)

        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = e
            base_DTO_obj.data_list = None

            part_list_serializer_DTO_reponse = Part_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(part_Serializer_DTO_reponse.data, safe=False)
   

@api_view(['GET', 'POST', 'DELETE'])
def edited_part(request):

    if request.method == 'POST':

        try:

            part_data = JSONParser().parse(request)

            base_DTO_obj =  base_DTO()

            if part_data['package_no'] is None or part_data['package_no'].strip() == "" :

                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("PART_MASTER_PACKAGENO_REQUIRED").data
                base_DTO_obj.data_list = None

                part_Serializer_DTO = Part_Serializer_DTO(base_DTO_obj)

                return JsonResponse(part_Serializer_DTO.data, safe=False) 

            
            elif part_data['package_volume'] is None or part_data['package_volume'] == "" :

                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("PART_MASTER_PACKAGEVOLUME_REQUIRED").data
                base_DTO_obj.data_list = None

                part_Serializer_DTO = Part_Serializer_DTO(base_DTO_obj)

                return JsonResponse(part_Serializer_DTO.data, safe=False) 
            
            elif part_data['package_weight'] is None or part_data['package_weight'] == "" :

                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("PART_MASTER_PACKAGEWEIGHT_REQUIRED").data
                base_DTO_obj.data_list = None

                part_Serializer_DTO = Part_Serializer_DTO(base_DTO_obj)

                return JsonResponse(part_Serializer_DTO.data, safe=False) 
            
            else :

                part_obj = Part.objects.filter( part_number = part_data["part_number"] )
                part_serializer_obj = Part_Serializer(part_obj[0],data=part_data)

                if part_serializer_obj.is_valid():

                    part_serializer_obj.save()
                    
                    base_DTO_obj =  base_DTO()
                    base_DTO_obj.serviceStatus = "success"
                    base_DTO_obj.massage = configMessage.configs.get("PART_MASTER_EDIT_MASSAGE_SUCCESSFUL").data
                    base_DTO_obj.data_list = Part.objects.all()

                    part_list_serializer_DTO_reponse = Part_list_Serializer_DTO(base_DTO_obj)

                    return JsonResponse(part_list_serializer_DTO_reponse.data, safe=False)

                else :  
                    
                    part_serializer_obj.save()
                    
                    base_DTO_obj =  base_DTO()
                    base_DTO_obj.serviceStatus = "Error"
                    base_DTO_obj.massage = part_serializer_obj.errors
                    base_DTO_obj.data_list = Part.objects.all()

                    part_list_serializer_DTO_reponse = Part_list_Serializer_DTO(base_DTO_obj)

                    return JsonResponse(part_list_serializer_DTO_reponse.data, safe=False)
        

        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = e
            base_DTO_obj.data = None

            print(e)

            part_Serializer_DTO_reponse = Part_Serializer_DTO(base_DTO_obj)

            return JsonResponse(part_Serializer_DTO_reponse.data, safe=False)

@api_view(['POST'])



def seach_part(request):

    if request.method == 'POST':

        try:

            part_data_obj = JSONParser().parse(request)

            customer_selected = part_data_obj['customer_selected']
            project_selected = part_data_obj['project_selected']
            supplier_selected = part_data_obj['supplier_selected']
            status_selected = part_data_obj['status_selected']
            partNumber_selected = part_data_obj['partNumber_selected']

            query = "select * from master_data_part "

            joint_str = "" 
            where_str = " where 1 = 1 and master_data_part.is_active = true "

            if customer_selected is not None and customer_selected != "":
                
                joint_str = joint_str + " INNER JOIN master_data_project "
                joint_str = joint_str + " ON UPPER(master_data_project.project_code) = UPPER(master_data_part.project_code) "

                joint_str = joint_str + " INNER JOIN master_data_customer "
                joint_str = joint_str + " ON UPPER(master_data_customer.customer_code) = UPPER(master_data_project.customer_code) "
                where_str = where_str + " and  UPPER(master_data_project.customer_code) = '%s' " % customer_selected.upper()
            
            if project_selected is not None and project_selected != "":

                where_str = where_str + " and  UPPER(master_data_part.project_code) = '%s' " % project_selected.upper()

            if supplier_selected is not None and supplier_selected !="" :

                where_str = where_str + " and  UPPER(master_data_part.supplier_code) = '%s' " % supplier_selected.upper()

            if status_selected is not None:

                where_str = where_str + " and  master_data_part.status = '%s' " % status_selected
            
            if partNumber_selected and partNumber_selected != "":

                partNumber_selected = "%"+partNumber_selected+"%"
                where_str = where_str + " and  master_data_part.part_number LIKE '%%%s%%'  " %  partNumber_selected
            
            query = query + joint_str + where_str + " order by master_data_part.updated_date desc"

            print(query)

            part_list = Part.objects.raw(query)

            part_csv_list = []

            part_csv_list.insert(0, [
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
                        "Update Time Stamp",
                    ]
                )
            
            for part_obj in part_list:

                part_row_list = (
                    part_obj.project_code,
                    "Draft" if part_obj.status == 1 else "Confirm" ,
                    part_obj.supplier_code,
                    part_obj.part_number,
                    part_obj.part_name,
                    part_obj.package_no,
                    part_obj.package_volume,
                    part_obj.package_weight,
                    part_obj.remark,
                    part_obj.updated_by,
                    part_obj.updated_date.strftime("%d/%m/%Y"),

                    )
                
                part_csv_list.append(part_row_list)

            name_csv_str = "PartMasterCSV" +datetime.now().strftime("%Y%m%d_%H%M%S")

            with open("media/" +  name_csv_str +'.csv', 'w', newline='',encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(part_csv_list)

            
            part_serializer = Part_Serializer(part_list, many=True)


            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "success"
            base_DTO_obj.massage = "get part"
            base_DTO_obj.data_list = part_serializer.data
            base_DTO_obj.csv_name =  name_csv_str + '.csv'

            part_list_Serializer_DTO = Part_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(part_list_Serializer_DTO.data,safe=False)

        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = e
            base_DTO_obj.data = None

            part_Serializer_DTO_reponse = Part_Serializer_DTO(base_DTO_obj)

            return JsonResponse(part_Serializer_DTO_reponse.data, safe=False)


@api_view(['GET', 'POST', 'DELETE'])
def deleted_part(request):

    if request.method == 'POST':

        try:

            part_data = JSONParser().parse(request)

            print(part_data)
            part_list = Part.objects.filter(part_number__in=part_data)
            print(len(part_list))
            part_list.update(is_active = False)

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "success"
            base_DTO_obj.massage = configMessage.configs.get("PART_MASTER_DELETE_MASSAGE_SUCCESSFUL").data
            base_DTO_obj.data_list = Part.objects.filter(is_active=True)

            part_list_serializer_DTO_reponse = Part_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(part_list_serializer_DTO_reponse.data, safe=False) 
            
            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = part_serializer_obj.errors
            base_DTO_obj.data = None

            part_Serializer_DTO_reponse = Part_Serializer_DTO(base_DTO_obj)

            return JsonResponse(part_Serializer_DTO_reponse.data,safe=False)

        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = e
            base_DTO_obj.data = None

            project_Serializer_DTO_reponse = Project_Serializer_DTO(base_DTO_obj)

            return JsonResponse(project_Serializer_DTO_reponse.data, safe=False)


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
            station_list = Station.objects.filter(station_type = 'SUPPLIER')
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
# @permission_classes([IsAuthenticated])

def plant_list(request):
    

    if request.method == 'GET':
        try:
            station_list = Station.objects.filter(station_type = 'PLANT')
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
            # base_DTO_obj.data_list = order_serializer.data

            station_list_Serializer_DTO_obj = Station_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(station_list_Serializer_DTO_obj.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'DELETE'])
def project_list(request):

    if request.method == 'GET':

        try : 

            project_list = Project.objects.filter(is_active=True)
            project_serializer = Project_Serializer(project_list, many=True, context={'request': 'test'})
            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "success"
            base_DTO_obj.massage = "get router"
            base_DTO_obj.data_list = project_serializer.data

            project_list_Serializer_DTO_obj = Project_list_Serializer_DTO(base_DTO_obj)


            return JsonResponse(project_list_Serializer_DTO_obj.data, safe=False)

        except Exception as e:

            print(e)
            return JsonResponse("sdfsdfsdfsdf", safe=False)

    elif request.method == 'POST':

        try:

            project_data_list = JSONParser().parse(request)
            

            for project_obj in project_data_list :

                project_list =  Project.objects.filter(project_code__iexact = project_obj['project_code'])

                if project_obj['project_code'] is None or project_obj['project_code'].strip() == "" :

                    base_DTO_obj =  base_DTO()
                    base_DTO_obj.serviceStatus = "Error"
                    base_DTO_obj.massage = configMessage.configs.get("PROJECT_MASTER_PROJECT_REQUIRED").data
                    base_DTO_obj.data_list = None

                    project_list_serializer_DTO_reponse = Project_list_Serializer_DTO(base_DTO_obj)

                    return JsonResponse(project_list_serializer_DTO_reponse.data, safe=False) 

                    break;
                
                if project_obj['customer_code'] is None or project_obj['customer_code'].strip() == "":

                    base_DTO_obj =  base_DTO()
                    base_DTO_obj.serviceStatus = "Error"
                    base_DTO_obj.massage = configMessage.configs.get("PROJECT_MASTER_CUSTOMER_REQUIRED").data
                    base_DTO_obj.data_list = None

                    project_list_serializer_DTO_reponse = Project_list_Serializer_DTO(base_DTO_obj)

                    return JsonResponse(project_list_serializer_DTO_reponse.data, safe=False) 

                    break;


                if len (project_list) :

                    
                    if project_list[0].is_active:

                        base_DTO_obj =  base_DTO()
                        base_DTO_obj.serviceStatus = "Error"
                        base_DTO_obj.massage = configMessage.configs.get("PROJECT_MASTER_DUPLICATE").data
                        base_DTO_obj.data_list = None

                        project_list_serializer_DTO_reponse = Project_list_Serializer_DTO(base_DTO_obj)

                        return JsonResponse(project_list_serializer_DTO_reponse.data, safe=False) 

                        break;
                    
                    else : 
                        
                        project_list.update(
                            project_code=project_obj['project_code'],
                            customer_code= project_obj['customer_code'],
                            remark= project_obj['remark'],
                            is_active=True
                            )
                        base_DTO_obj =  base_DTO()
                        base_DTO_obj.serviceStatus = "success"
                        base_DTO_obj.massage = configMessage.configs.get("PROJECT_MASTER_ADD_MASSAGE_SUCCESSFUL").data
                        base_DTO_obj.data_list = Project.objects.all()

                        project_list_serializer_DTO_reponse = Project_list_Serializer_DTO(base_DTO_obj)

                        return JsonResponse(project_list_serializer_DTO_reponse.data, safe=False)

            project_serializer_obj = Project_Serializer(data=project_data_list,many=True)

        

            if project_serializer_obj.is_valid():

                project_serializer_obj.save()
                # project_serializer_obj.save(updated_by=request.user.username,)

                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "success"
                base_DTO_obj.massage = configMessage.configs.get("PROJECT_MASTER_ADD_MASSAGE_SUCCESSFUL").data
                base_DTO_obj.data_list = Project.objects.all()

                project_list_serializer_DTO_reponse = Project_list_Serializer_DTO(base_DTO_obj)

                return JsonResponse(project_list_serializer_DTO_reponse.data, safe=False) 
            
            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = project_serializer_obj.errors
            base_DTO_obj.data = None

            project_Serializer_DTO_reponse = Project_Serializer_DTO(base_DTO_obj)

            return JsonResponse(project_Serializer_DTO_reponse.data,safe=False)

        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = e
            base_DTO_obj.data = None

            project_Serializer_DTO_reponse = Project_Serializer_DTO(base_DTO_obj)

            return JsonResponse(project_Serializer_DTO_reponse.data, safe=False)

@api_view(['GET', 'POST', 'DELETE'])
def deleted_project(request):

    if request.method == 'POST':

        try:

            project_data = JSONParser().parse(request)
            print(project_data)
    
            project_list = Project.objects.filter(project_code__in=project_data)
            project_list.update(is_active = False)

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "success"
            base_DTO_obj.massage = configMessage.configs.get("PROJECT_MASTER_DELETE_MASSAGE_SUCCESSFUL").data
            base_DTO_obj.data_list = Project.objects.all()

            project_list_serializer_DTO_reponse = Project_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(project_list_serializer_DTO_reponse.data, safe=False) 
            
            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = project_serializer_obj.errors
            base_DTO_obj.data = None

            project_Serializer_DTO_reponse = Project_Serializer_DTO(base_DTO_obj)

            return JsonResponse(project_Serializer_DTO_reponse.data,safe=False)

        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = e
            base_DTO_obj.data = None

            project_Serializer_DTO_reponse = Project_Serializer_DTO(base_DTO_obj)

            return JsonResponse(project_Serializer_DTO_reponse.data, safe=False)

@api_view(['GET', 'POST', 'DELETE'])
def edited_project(request):

    if request.method == 'POST':

        try:

            project_data = JSONParser().parse(request)
            project_obj = Project.objects.filter( project_code = project_data["project_code"] )
            project_serializer_obj = Project_Serializer(project_obj[0],data=project_data)

            if project_serializer_obj.is_valid():

                project_serializer_obj.save()
                    
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "success"
                base_DTO_obj.massage = configMessage.configs.get("PROJECT_MASTER_EDIT_MASSAGE_SUCCESSFUL").data
                base_DTO_obj.data_list = Project.objects.all()

                project_list_serializer_DTO_reponse = Project_list_Serializer_DTO(base_DTO_obj)

                return JsonResponse(project_list_serializer_DTO_reponse.data, safe=False) 

        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = e
            base_DTO_obj.data = None

            project_Serializer_DTO_reponse = Project_Serializer_DTO(base_DTO_obj)

            return JsonResponse(project_Serializer_DTO_reponse.data, safe=False)

@api_view(['POST'])
def seach_project(request):

    if request.method == 'POST':

        try:

            project_data_obj = JSONParser().parse(request)
            customer_selected = project_data_obj['customer_code']
            # project_selected = project_data_obj['project_code']

            query = "select * from master_data_project "

            joint_str = "" 
            where_str = " where 1 = 1 and master_data_project.is_active = True"

            if customer_selected is not None:

                # joint_str = joint_str + " INNER JOIN master_data_customer "
                # joint_str = joint_str + " ON master_data_customer.customer_code = master_data_project.project_code"
                where_str = where_str + " and  master_data_project.customer_code = '%s' " % customer_selected
            
            # if project_selected is not None :

            #     where_str = where_str + "and  master_data_project.project_code = '%s' " % project_selected
            
            query = query + joint_str + where_str + " ORDER BY master_data_project.updated_date desc"

            print(query)

            project_list = Project.objects.raw(query)

            project_csv_list = []

            project_csv_list.insert(0, [
                        "Project Code",
                        "Customer Code",
                        "Remark",
                        "Updated By",
                        "Updated Timestamp",
                    ]
                )
            
            for project_obj in project_list:

                print(project_obj)
                project_row_list = (
                    project_obj.project_code,
                    project_obj.customer_code,
                    project_obj.remark,
                    project_obj.updated_by,
                    project_obj.updated_date.strftime("%d/%m/%Y"),

                    )
                
                project_csv_list.append(project_row_list)

            name_csv_str = datetime.now().strftime("ProjectMasterCSV_%Y%d%m_-%H%M%S")
            with open("media/" +  name_csv_str +'.csv', 'w', newline='',encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(project_csv_list)

            
            project_serializer = Project_Serializer(project_list, many=True)


            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "success"
            base_DTO_obj.massage = "get part"
            base_DTO_obj.data_list = project_serializer.data
            base_DTO_obj.csv_name =  name_csv_str + '.csv'

            project_list_Serializer_DTO = Project_list_Serializer_DTO(base_DTO_obj)




            # project_serializer_obj = Project_Serializer(data=project_data)
            

            # if project_serializer_obj.is_valid():

            #     project_serializer_obj.save()
            #     project_serializer_obj.save(updated_by=request.user.username)

            #     base_DTO_obj =  base_DTO()
            #     base_DTO_obj.serviceStatus = "success"
            #     base_DTO_obj.massage = "save part is successful"
            #     base_DTO_obj.data_list = Project.objects.all()

            #     project_list_serializer_DTO_reponse = Project_list_Serializer_DTO(base_DTO_obj)

            #     return JsonResponse(project_list_serializer_DTO_reponse.data, safe=False) 
            
            # base_DTO_obj =  base_DTO()
            # base_DTO_obj.serviceStatus = "Error"
            # base_DTO_obj.massage = project_serializer_obj.errors
            # base_DTO_obj.data = None

            # project_Serializer_DTO_reponse = Project_Serializer_DTO(base_DTO_obj)

            return JsonResponse(project_list_Serializer_DTO.data,safe=False)

        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = e
            base_DTO_obj.data = None

            project_Serializer_DTO_reponse = Project_Serializer_DTO(base_DTO_obj)

            return JsonResponse(project_Serializer_DTO_reponse.data, safe=False)




    
    # if request.method == 'GET':
    #     try:
    #         project_list = Project.objects.all()
    #         project_serializer = Project_Serializer(project_list, many=True)

    #         base_DTO_obj =  base_DTO()
    #         base_DTO_obj.serviceStatus = "success"
    #         base_DTO_obj.massage = "get router"
    #         base_DTO_obj.data_list = project_serializer.data

    #         project_list_Serializer_DTO_obj = Project_list_Serializer_DTO(base_DTO_obj)

    #         return JsonResponse(project_list_Serializer_DTO_obj.data, status=status.HTTP_200_OK)
    #     except Exception as e:

    #         base_DTO_obj =  base_DTO()
    #         base_DTO_obj.serviceStatus = "error"
    #         base_DTO_obj.massage = e 
    #         # base_DTO_obj.data_list = order_serializer.data

    #         project_list_Serializer_DTO_obj = Project_list_Serializer_DTO(base_DTO_obj)

    #         return JsonResponse(project_list_Serializer_DTO_obj.data, status=status.HTTP_200_OK)

        

    #         # return JsonResponse(order_serializer.data, safe=False)

    # elif request.method == 'POST':


    #     try:
    #         project_data = JSONParser().parse(request)
    #         project_serializer_obj = Project_Serializer(data=project_data)
            

    #         if project_serializer_obj.is_valid():

    #             project_serializer_obj.save()

    #             base_DTO_obj =  base_DTO()
    #             base_DTO_obj.serviceStatus = "success"
    #             base_DTO_obj.massage = "save part is successful"
    #             base_DTO_obj.data = project_serializer_obj.data

    #             project_Serializer_DTO_reponse = Project_Serializer_DTO(base_DTO_obj)

    #             return JsonResponse(project_Serializer_DTO_reponse.data, status=status.HTTP_201_CREATED) 
            
    #         base_DTO_obj =  base_DTO()
    #         base_DTO_obj.serviceStatus = "Error"
    #         base_DTO_obj.massage = project_serializer_obj.errors
    #         base_DTO_obj.data = None

    #         project_Serializer_DTO_reponse = Project_Serializer_DTO(base_DTO_obj)

    #         return JsonResponse(project_Serializer_DTO_reponse.data, status=status.HTTP_400_BAD_REQUEST)

    #     except Exception as e:

    #         base_DTO_obj =  base_DTO()
    #         base_DTO_obj.serviceStatus = "Error"
    #         base_DTO_obj.massage = e
    #         base_DTO_obj.data = None

    #         project_Serializer_DTO_reponse = Project_Serializer_DTO(base_DTO_obj)

    #         return JsonResponse(project_Serializer_DTO_reponse.data, status=status.HTTP_200_OK)





@api_view(['GET', 'POST', 'DELETE'])
def customer_list(request):
    
    if request.method == 'GET':
        try:
            customer_list = Customer.objects.all()
            print(customer_list)
            customer_serializer_obj = Customer_Serializer(customer_list, many=True)

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "success"
            base_DTO_obj.massage = "get router"
            base_DTO_obj.data_list = customer_serializer_obj.data

            customer_list_Serializer_DTO_obj = Customer_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(customer_list_Serializer_DTO_obj.data, status=status.HTTP_200_OK)
        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "error"
            base_DTO_obj.massage = e 
            # base_DTO_obj.data_list = order_serializer.data

            customer_list_Serializer_DTO_obj = Customer_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(customer_list_Serializer_DTO_obj.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':

        try:
            customer_data = JSONParser().parse(request)
         

            if customer_data['project_code'] is None or customer_data['project_code'].strip() == "" :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("STATION_MASTER_PROJECT_REQUIRED").data
                base_DTO_obj.data = None

                customer_Serializer_DTO_reponse = Customer_Serializer_DTO(base_DTO_obj)

                return JsonResponse(customer_Serializer_DTO_reponse.data, status=status.HTTP_200_OK) 
            
            if customer_data['station_code'] is None or customer_data['station_code'].strip() == "" :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("STATION_MASTER_STATIONCODE_REQUIRED").data
                base_DTO_obj.data = None

                customer_Serializer_DTO_reponse = Customer_Serializer_DTO(base_DTO_obj)

                return JsonResponse(customer_Serializer_DTO_reponse.data, status=status.HTTP_200_OK) 

            if customer_data['description'] is None or customer_data['description'].strip() == "" :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("STATION_MASTER_DESCRIPTION_REQUIRED").data
                base_DTO_obj.data = None

                customer_Serializer_DTO_reponse = Customer_Serializer_DTO(base_DTO_obj)

                return JsonResponse(customer_Serializer_DTO_reponse.data, status=status.HTTP_200_OK) 
            
            if customer_data['station_type'] is None or customer_data['station_type'].strip() == "" :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("STATION_MASTER_TYPE_REQUIRED").data
                base_DTO_obj.data = None

                customer_Serializer_DTO_reponse = Customer_Serializer_DTO(base_DTO_obj)

                return JsonResponse(customer_Serializer_DTO_reponse.data, status=status.HTTP_200_OK) 
            
            if customer_data['zone'] is None or customer_data['zone'].strip() == "" :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("STATION_MASTER_ZONE_REQUIRED").data
                base_DTO_obj.data = None

                customer_Serializer_DTO_reponse = Customer_Serializer_DTO(base_DTO_obj)

                return JsonResponse(customer_Serializer_DTO_reponse.data, status=status.HTTP_200_OK)
            
            if customer_data['province'] is None or customer_data['province'].strip() == "" :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("STATION_MASTER_PROVINCE_REQUIRED").data
                base_DTO_obj.data = None

                customer_Serializer_DTO_reponse = Customer_Serializer_DTO(base_DTO_obj)

                return JsonResponse(customer_Serializer_DTO_reponse.data, status=status.HTTP_200_OK)
            
            if customer_data['address'] is None or customer_data['address'].strip() == "" :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("STATION_MASTER_ADDRESS_REQUIRED").data
                base_DTO_obj.data = None

                customer_Serializer_DTO_reponse = Customer_Serializer_DTO(base_DTO_obj)

                return JsonResponse(customer_Serializer_DTO_reponse.data, status=status.HTTP_200_OK)


            station_list = Station.objects.filter(station_code = customer_data['station_code'])
            
            if len(station_list) >0:


                if station_list[0].is_active is True : 

                    base_DTO_obj =  base_DTO()
                    base_DTO_obj.serviceStatus = "Error"
                    base_DTO_obj.massage = configMessage.configs.get("STATION_MASTER_DUPLICATE").data
                    base_DTO_obj.data = None

                    customer_Serializer_DTO_reponse = Customer_Serializer_DTO(base_DTO_obj)

                    return JsonResponse(customer_Serializer_DTO_reponse.data, status=status.HTTP_200_OK) 
                
                else :
                    
                    station_list.update(
                        project_code=customer_data['project_code'],
                        description= customer_data['description'],
                        station_type= customer_data['station_type'],
                        zone= customer_data['zone'],
                        province= customer_data['province'],
                        address= customer_data['address'],
                        remark= customer_data['remark'],
                        is_active = True
                    
                    )

                    if customer_data['station_type'] == "PLANT":

                        calendarMaster_list = CalendarMaster.objects.filter(plant_code__iexact=customer_data['station_code'])
                        if len(calendarMaster_list) > 0 :

                            calendarMaster_list.update(is_active = True)
                    
                        else:

                            start_date = datetime(datetime.now().year+1, 1, 1)
                            end_date = datetime(2021, 12, 31)
                            daterange = pd.date_range(start_date, end_date)
                            for single_date in daterange:

                                calendarMaster_obj =  CalendarMaster()
                                calendarMaster_obj.plant_code = customer_data['station_code']
                                day_int = int(single_date.strftime("%w")) + 1
                                calendarMaster_obj.day = day_int
                                calendarMaster_obj.date = single_date
                                
                                if day_int == 1 :

                                    calendarMaster_obj.is_working =  False 
                                
                                else : 

                                    calendarMaster_obj.is_working = True
                                
                                calendarMaster_obj.updated_by = request.user.username
                                calendarMaster_obj.updated_date = datetime.utcnow()
                                calendarMaster_obj.is_active = True

                                calendarMaster_obj.save()
                    
                    base_DTO_obj =  base_DTO()
                    base_DTO_obj.serviceStatus = "success"
                    base_DTO_obj.massage = configMessage.configs.get("STATION_MASTER_ADD_MASSAGE_SUCCESSFUL").data
                    base_DTO_obj.data = None

                    customer_Serializer_DTO_reponse = Customer_Serializer_DTO(base_DTO_obj)

                    return JsonResponse(customer_Serializer_DTO_reponse.data, status=status.HTTP_200_OK)

            customer_serializer_obj = Customer_Serializer(data=customer_data)

            
            if customer_serializer_obj.is_valid():

                customer_serializer_obj.save()
                print(customer_data['station_type'])

                if customer_data['station_type'] == "PLANT":

                    start_date = datetime(datetime.now().year+1, 1, 1)
                    end_date = datetime(datetime.now().year+1, 12, 31)
                    daterange = pd.date_range(start_date, end_date)
                    for single_date in daterange:

                        calendarMaster_obj =  CalendarMaster()
                        calendarMaster_obj.plant_code = customer_data['station_code']
                        day_int = int(single_date.strftime("%w")) + 1
                        calendarMaster_obj.day = day_int
                        calendarMaster_obj.date = single_date
                        
                        if day_int == 1 :

                            calendarMaster_obj.is_working =  False 
                        
                        else : 

                            calendarMaster_obj.is_working = True
                        
                        calendarMaster_obj.updated_by = request.user.username
                        calendarMaster_obj.updated_date = datetime.now()
                        calendarMaster_obj.is_active = True

                        calendarMaster_obj.save()
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "success"
                base_DTO_obj.massage = configMessage.configs.get("STATION_MASTER_ADD_MASSAGE_SUCCESSFUL").data
                base_DTO_obj.data = customer_serializer_obj.data

                customer_Serializer_DTO_reponse = Customer_Serializer_DTO(base_DTO_obj)

                return JsonResponse(customer_Serializer_DTO_reponse.data, status=status.HTTP_201_CREATED) 
            
            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = customer_serializer_obj.errors
            base_DTO_obj.data = None

            customer_Serializer_DTO_reponse = Customer_Serializer_DTO(base_DTO_obj)

            return JsonResponse(customer_Serializer_DTO_reponse.data, status=status.HTTP_200_OK)

        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = e
            base_DTO_obj.data = None

            customer_Serializer_DTO_reponse = Customer_Serializer_DTO(base_DTO_obj)

        return JsonResponse(customer_Serializer_DTO_reponse.data, status=status.HTTP_200_OK)



@api_view(['GET', 'POST', 'DELETE'])
def deleted_customer(request):

    if request.method == 'POST':

        try:

            station_data = JSONParser().parse(request)
            station_list = Station.objects.filter(station_code__in=station_data)
            station_list.update(is_active = False)

            calendarMaster_list = CalendarMaster.objects.filter(plant_code__in=station_data)
            calendarMaster_list.update(is_active = False)

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "success"
            base_DTO_obj.massage = configMessage.configs.get("STATION_MASTER_DELETE_MASSAGE_SUCCESSFUL").data
            base_DTO_obj.data_list = None

            customer_list_serializer_DTO_reponse = Customer_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(customer_list_serializer_DTO_reponse.data, safe=False) 
            

        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = e
            base_DTO_obj.data = None

            customer_list_Serializer_DTO = Customer_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(customer_list_Serializer_DTO.data, safe=False)


@api_view(['GET', 'POST', 'DELETE'])
def edited_customer(request):

    if request.method == 'POST':

        try:

            customer_data = JSONParser().parse(request)

            # print(customer_data)

            if customer_data['description'] is None or customer_data['description'].strip() == "" :
                
                print("description is error")
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("STATION_MASTER_DESCRIPTION_REQUIRED").data
                base_DTO_obj.data = None

                customer_Serializer_DTO = Customer_Serializer_DTO(base_DTO_obj)

                return JsonResponse(customer_Serializer_DTO.data, status=status.HTTP_200_OK) 
            
            if customer_data['station_type'] is None or customer_data['station_type'].strip() == "" :
                
                print("station_type")
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("STATION_MASTER_TYPE_REQUIRED").data
                base_DTO_obj.data = None

                customer_Serializer_DTO_reponse = Customer_Serializer_DTO(base_DTO_obj)

                return JsonResponse(customer_Serializer_DTO_reponse.data, status=status.HTTP_200_OK) 
            
            if customer_data['zone'] is None or customer_data['zone'].strip() == "" :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("STATION_MASTER_ZONE_REQUIRED").data
                base_DTO_obj.data = None

                customer_Serializer_DTO_reponse = Customer_Serializer_DTO(base_DTO_obj)

                return JsonResponse(customer_Serializer_DTO_reponse.data, status=status.HTTP_200_OK)
            
            if customer_data['province'] is None or customer_data['province'].strip() == "" :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("STATION_MASTER_PROVINCE_REQUIRED").data
                base_DTO_obj.data = None

                customer_Serializer_DTO_reponse = Customer_Serializer_DTO(base_DTO_obj)

                return JsonResponse(customer_Serializer_DTO_reponse.data, status=status.HTTP_200_OK)
            
            if customer_data['address'] is None or customer_data['address'].strip() == "" :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("STATION_MASTER_ADDRESS_REQUIRED").data
                base_DTO_obj.data = None

                customer_Serializer_DTO_reponse = Customer_Serializer_DTO(base_DTO_obj)

                return JsonResponse(customer_Serializer_DTO_reponse.data, status=status.HTTP_200_OK) 

      
            station_obj = Station.objects.filter( station_code = customer_data["station_code"] )
            customer_serializer_obj = Customer_Serializer(station_obj[0],data=customer_data)
            

            if customer_serializer_obj.is_valid():

                customer_serializer_obj.save()

                if customer_data['station_type'] is "PLANT":

                    calendarMaster_list = CalendarMaster.objects.filter(plant_code = customer_data['station_type'])
                    if len(calendarMaster_list) > 0 :

                        calendarMaster_list.update(is_active = True)
                    
                    else:

                        start_date = datetime(datetime.now().year+1, 1, 1)
                        end_date = datetime(2021, 12, 31)
                        daterange = pd.date_range(start_date, end_date)
                        for single_date in daterange:

                            calendarMaster_obj =  CalendarMaster()
                            calendarMaster_obj.plant_code = customer_data['station_code']
                            day_int = int(single_date.strftime("%w")) + 1
                            calendarMaster_obj.day = day_int
                            calendarMaster_obj.date = single_date
                            
                            if day_int == 1 :

                                calendarMaster_obj.is_working =  False 
                            
                            else : 

                                calendarMaster_obj.is_working = True
                            
                            calendarMaster_obj.updated_by = request.user.username
                            calendarMaster_obj.updated_date = datetime.now()
                            calendarMaster_obj.is_active = True

                            calendarMaster_obj.save()
                            

                    

                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "success"
                base_DTO_obj.massage = configMessage.configs.get("STATION_MASTER_EDIT_MASSAGE_SUCCESSFUL").data
                base_DTO_obj.data = None

                customer_Serializer_DTO = Customer_Serializer_DTO(base_DTO_obj)

                return JsonResponse(customer_Serializer_DTO.data, safe=False) 
            
        

        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = e
            base_DTO_obj.data = None

            print(e)

            project_Serializer_DTO_reponse = Project_Serializer_DTO(base_DTO_obj)

            return JsonResponse(project_Serializer_DTO_reponse.data, safe=False)


@api_view(['POST'])
def seach_customer(request):

    if request.method == 'POST':

        try:

            customer_data_obj = JSONParser().parse(request)
            project_selected = customer_data_obj['project_code']
            customer_selected = customer_data_obj['customer_code']
            stationCode_selected = customer_data_obj['stationCode_selected']

            print(customer_data_obj)

            query = "select * from master_data_station "

            joint_str = "" 
            where_str = " where 1 = 1 and master_data_station.is_active = true "

            if customer_selected is not None and  customer_selected is not "":

                joint_str = joint_str + " INNER JOIN master_data_project "
                joint_str = joint_str + " ON UPPER(master_data_project.project_code) = UPPER(master_data_station.project_code) "
                joint_str = joint_str + " INNER JOIN master_data_customer "
                joint_str = joint_str + " ON UPPER(master_data_customer.customer_code) = UPPER(master_data_project.customer_code) "
                where_str = where_str + " and  UPPER(master_data_customer.customer_code) = '%s' " % customer_selected.upper()
                    

            if project_selected is not None and  project_selected is not "":

                where_str = where_str + " and  UPPER(master_data_station.project_code) = '%s' " % project_selected.upper()

            if stationCode_selected is not None and  stationCode_selected is not "":

                stationCode_selected = "%"+stationCode_selected+"%"
                where_str = where_str + " and  master_data_station.station_code LIKE '%%%s%%'  " %  stationCode_selected
            
            
            query = query + joint_str + where_str + "order by master_data_station.updated_date desc"

            print(query)
            station_list = Station.objects.raw(query)

            station_csv_list = []

            station_csv_list.insert(0, [
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
                        "Update Time"
                    ]
                )
            
            customer_list = []
            
            for station_obj in station_list:

                project_list = Project.objects.filter(project_code = station_obj.project_code )
                customer_code = ""

                if len(project_list) > 0 :
                    customer_code = project_list[0].customer_code


                customer_DTO =  Customer_DTO()
                customer_DTO.station_code = station_obj.station_code
                customer_DTO.project_code = station_obj.project_code
                customer_DTO.description = station_obj.description
                customer_DTO.station_type = station_obj.station_type
                customer_DTO.zone = station_obj.zone
                customer_DTO.province = station_obj.province
                customer_DTO.address = station_obj.address
                customer_DTO.remark = station_obj.remark
                customer_DTO.updated_by = station_obj.updated_by
                customer_DTO.updated_date = station_obj.updated_date

                customer_list.append(customer_DTO)

    
                station_row_list = (
                    customer_code,
                    station_obj.project_code,
                    station_obj.station_code,
                    station_obj.description,
                    station_obj.station_type,
                    station_obj.zone,
                    station_obj.province,
                    station_obj.address,
                    station_obj.remark,
                    station_obj.updated_by,
                    station_obj.updated_date.strftime("%d/%m/%Y")
                    )
                
                station_csv_list.append(station_row_list)

            name_csv_str = "CustomerMasterCSV" +datetime.now().strftime("%Y%m%d_%H%M%S")

            with open("media/" +  name_csv_str +'.csv', 'w', newline='',encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(station_csv_list)

            print(customer_list)
            
            customer_serializer = Customer_Serializer(customer_list, many=True)


            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "success"
            base_DTO_obj.massage = "Get Customer"
            base_DTO_obj.data_list = customer_serializer.data
            base_DTO_obj.csv_name =  name_csv_str + '.csv'

            customer_list_Serializer_DTO = Customer_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(customer_list_Serializer_DTO.data,safe=False)

        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = e
            base_DTO_obj.data = None

            project_Serializer_DTO_reponse = Project_Serializer_DTO(base_DTO_obj)

            return JsonResponse(project_Serializer_DTO_reponse.data, safe=False)

@api_view(['GET', 'POST', 'DELETE'])
def package_list(request):
    
    if request.method == 'GET':
        try:
            package_list = Package.objects.filter(is_active=True)
            package_serializer_obj = Package_Serializer(package_list, many=True)

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "success"
            base_DTO_obj.massage = "get package"
            base_DTO_obj.data_list = package_serializer_obj.data

            package_list_Serializer_DTO_obj = Package_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(package_list_Serializer_DTO_obj.data, status=status.HTTP_200_OK)
        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "error"
            base_DTO_obj.massage = e 
            # base_DTO_obj.data_list = order_serializer.data

            package_list_Serializer_DTO_obj = Package_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(package_list_Serializer_DTO_obj.data, status=status.HTTP_200_OK)

        

            # return JsonResponse(order_serializer.data, safe=False)

    elif request.method == 'POST':

        try:

            # package_data = JSONParser().parse(request.POST['packages'])
            # upload_route_master_file = request.FILES['file']

            base_DTO_obj =  base_DTO()

            if request.POST['station_code'] == "null" or request.POST['station_code'] == "" :

                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("PACKAGES_MASTER_STATIONCODE_REQUIRED").data

            elif request.POST['package_code'] == "null" or request.POST['package_code'] == "" :

                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("PACKAGES_MASTER_PACKAGECODE_REQUIRED").data
            
            elif request.POST['package_no'] == "null" or request.POST['package_no'] == "" :

                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("PACKAGES_MASTER_PACKAGENO_REQUIRED").data
            
            elif request.POST['snp'] == "null" or request.POST['snp'] == "" :

                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("PACKAGES_MASTER_SNP_REQUIRED").data
            
            elif int(request.POST['snp']) <= 0 :

                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("PACKAGES_MASTER_SNP_MORE_THAN_ZERO").data

            elif request.POST['width'] == "null" or request.POST['width'] == "" :

                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("PACKAGES_MASTER_WIDTH_REQUIRED").data
            
            elif request.POST['length'] == "null" or request.POST['length'] == "" :

                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("PACKAGES_MASTER_LENGTH_REQUIRED").data
            
            elif request.POST['height'] == "null"  or request.POST['height'] == "" :

                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("PACKAGES_MASTER_HEIGHT_REQUIRED").data
            
            elif request.POST['weight'] == "null" or request.POST['weight'] == "" :

                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("PACKAGES_MASTER_WEIGHT_REQUIRED").data

            else :

                try:

                    image_obj = request.FILES['file']
                    image_name_str = request.POST['package_no']
                    fs = FileSystemStorage(location="media/") #defaults to   MEDIA_ROOT  
                    file_name_str = fs.save(image_name_str, image_obj)
                    image_url = image_name_str
                    
                except:

                    image_url = ""
                
                package_list = Package.objects.filter(package_no=request.POST['package_no'])
                if len(package_list) > 0 :

                    if package_list[0].is_active == True :

                        base_DTO_obj.serviceStatus = "Error"
                        base_DTO_obj.massage = configMessage.configs.get("PACKAGES_MASTER_DUPLICATE").data
                        base_DTO_obj.data = base_DTO_obj

                        package_Serializer_DTO_reponse = Package_Serializer_DTO(base_DTO_obj)

                        return JsonResponse(package_Serializer_DTO_reponse.data, status=status.HTTP_200_OK)


                    else :
                        package_list.update(
                            package_code = request.POST['package_code'],
                            package_no = request.POST['package_no'],
                            snp= int(request.POST['snp']),
                            width = Decimal(request.POST['width']),
                            length = Decimal(request.POST['length']),
                            height = Decimal(request.POST['height']),
                            weight = Decimal(request.POST['weight']),
                            image_url = image_url,
                            is_active=True
                        )
                    

                
                else:
                    package = Package()
                    package.package_code = request.POST['package_code']
                    package.package_no = request.POST['package_no']
                    package.snp = request.POST['snp']
                    package.width = Decimal(request.POST['width'])
                    package.length = Decimal(request.POST['length'])
                    package.height = Decimal(request.POST['height'])
                    package.weight = Decimal(request.POST['weight'])
                    package.image_url = image_url
                    package.station_code = request.POST['station_code']
                    package.is_active = True
                    package.updated_by = request.user.username

                    package.save()

                base_DTO_obj.serviceStatus = "success"
                base_DTO_obj.massage = configMessage.configs.get("PACKAGES_MASTER_ADD_MASSAGE_SUCCESSFUL").data
                base_DTO_obj.data = base_DTO_obj



            package_Serializer_DTO_reponse = Package_Serializer_DTO(base_DTO_obj)

            return JsonResponse(package_Serializer_DTO_reponse.data, status=status.HTTP_200_OK)
               

        except Exception as e:


            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = e
            base_DTO_obj.data = None

            package_Serializer_DTO_reponse = Package_Serializer_DTO(base_DTO_obj)

            return JsonResponse(package_Serializer_DTO_reponse.data, status=status.HTTP_200_OK)
        

     

@api_view(['GET', 'POST', 'DELETE'])
def deleted_package(request):

     if request.method == 'POST':

        try:

            package_data = JSONParser().parse(request)
            package_list = Package.objects.filter(package_no__in=package_data)
            package_list.update(is_active = False)


            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "success"
            base_DTO_obj.massage = configMessage.configs.get("PACKAGES_MASTER_DELETE_MASSAGE_SUCCESSFUL").data
            base_DTO_obj.data_list = None

            package_list_serializer_DTO_reponse = Package_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(package_list_serializer_DTO_reponse.data, safe=False) 
            

        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = e
            base_DTO_obj.data = None

            package_list_Serializer_DTO = Package_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(package_list_Serializer_DTO.data, safe=False)

      
        

@api_view(['GET', 'POST', 'DELETE'])
def edited_package(request):

    if request.method == 'POST':

        try:

            base_DTO_obj =  base_DTO()
            
            if request.POST['snp'] == "null" or request.POST['snp'] == "" :

                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("PACKAGES_MASTER_SNP_REQUIRED").data
            
            elif int(request.POST['snp']) <= 0 :

                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("PACKAGES_MASTER_SNP_MORE_THAN_ZERO").data

            elif request.POST['width'] == "null" or request.POST['width'] == "" :

                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("PACKAGES_MASTER_WIDTH_REQUIRED").data
            
            elif request.POST['length'] == "null" or request.POST['length'] == "" :

                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("PACKAGES_MASTER_LENGTH_REQUIRED").data
            
            elif request.POST['height'] == "null"  or request.POST['height'] == "" :

                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("PACKAGES_MASTER_HEIGHT_REQUIRED").data
            
            elif request.POST['weight'] == "null" or request.POST['weight'] == "" :

                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("PACKAGES_MASTER_WEIGHT_REQUIRED").data

            else :

                image_url = request.POST['image_url']

                try:

                    image_obj = request.FILES['file']
                    image_name_str = "image_" +datetime.now().strftime("%Y%m%d_%H%M%S")+".png"
                    fs = FileSystemStorage(location="media/") #defaults to   MEDIA_ROOT  
                    file_name_str = fs.save(image_name_str, image_obj)
                    image_url = image_name_str
                    
                except:

                    image_url = request.POST['image_url']
                
                package_updated_obj = Package.objects.filter(package_no=request.POST['package_no'])
                package_updated_obj.update(
                    snp=int(request.POST['snp']),
                    width=Decimal(request.POST['width']),
                    length=Decimal(request.POST['length']),
                    height=Decimal(request.POST['height']),
                    weight=Decimal(request.POST['weight']),
                    image_url=image_url
                )
                package_updated_obj.snp = int(request.POST['snp'])
                package_updated_obj.width = Decimal(request.POST['width'])
                package_updated_obj.length = Decimal(request.POST['length'])
                package_updated_obj.height = Decimal(request.POST['height'])
                package_updated_obj.weight = Decimal(request.POST['weight'])
                package_updated_obj.image_url = image_url

                

                base_DTO_obj.serviceStatus = "success"
                base_DTO_obj.massage = configMessage.configs.get("PACKAGES_MASTER_EDIT_MASSAGE_SUCCESSFUL").data
                base_DTO_obj.data = base_DTO_obj



            package_Serializer_DTO_reponse = Package_Serializer_DTO(base_DTO_obj)

            return JsonResponse(package_Serializer_DTO_reponse.data, status=status.HTTP_200_OK)
               

        except Exception as e:


            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = e
            base_DTO_obj.data = None

            package_Serializer_DTO_reponse = Package_Serializer_DTO(base_DTO_obj)

            return JsonResponse(package_Serializer_DTO_reponse.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def seach_package(request):

    if request.method == 'POST':

        try:

            package_data_obj = JSONParser().parse(request)

            customer_selected = package_data_obj['customer_selected']
            project_selected = package_data_obj['project_selected']
            supplier_selected = package_data_obj['supplier_selected']
            packageCode_selected = package_data_obj['packageCode_selected']
            packageNo_selected = package_data_obj['packageNo_selected']

            query = "select * from master_data_package "

            joint_str = "" 
            where_str = " where 1 = 1 and master_data_package.is_active = true "

            if customer_selected is not None and customer_selected != "":
                
                joint_str = joint_str + " INNER JOIN master_data_station "
                joint_str = joint_str + " ON UPPER(master_data_station.station_code) = UPPER(master_data_package.station_code) "

                joint_str = joint_str + " INNER JOIN master_data_project "
                joint_str = joint_str + " ON UPPER(master_data_project.project_code) = UPPER(master_data_station.project_code) "

                joint_str = joint_str + " INNER JOIN master_data_customer "
                joint_str = joint_str + " ON UPPER(master_data_customer.customer_code) = UPPER(master_data_project.customer_code) "
                
                where_str = where_str + " and   UPPER(master_data_customer.customer_code) = '%s' " % customer_selected.upper()

            if project_selected is not None and project_selected != "":

                where_str = where_str + " and   UPPER(master_data_project.project_code) = '%s' " % project_selected.upper()
            
            if supplier_selected is not None and supplier_selected != "" :

                where_str = where_str + "and  UPPER(master_data_package.station_code) = '%s' " % supplier_selected.upper()
            
            if packageCode_selected is not None and packageCode_selected != "" :

                packageCode_selected = "%"+packageCode_selected+"%"
                where_str = where_str + " and  master_data_package.package_code LIKE '%%%s%%'  " %  packageCode_selected
            
            if packageNo_selected is not None and packageNo_selected != "" :

                packageNo_selected = "%"+packageNo_selected+"%"
                where_str = where_str + " and  master_data_package.package_no LIKE '%%%s%%'  " %  packageNo_selected

            
            query = query + joint_str + where_str + " order by master_data_package.updated_date desc"


            package_list = Package.objects.raw(query)
            

            package_csv_list = []

            package_csv_list.insert(0, [
                        "Supplier Code",
                        "Package Code",
                        "Package No",
                        "W (mm.)",
                        "L (mm.)",
                        "H (mm.)",
                        "Weight (Kg)",
                        "Is There Image",
                        "Update By",
                        "Update Time Stamp",
                    ]
                )
            
            print(query)
            for package_obj in package_list:

                package_row_list = (
                    package_obj.station_code,
                    package_obj.package_code,
                    package_obj.package_no,
                    package_obj.width,
                    package_obj.length,
                    package_obj.height,
                    package_obj.weight,
                    "Yes" if package_obj.image_url is not None and not package_obj.image_url == "" else "No",
                    package_obj.updated_by,
                    package_obj.updated_date.strftime("%d/%m/%Y"),

                    )
                
                package_csv_list.append(package_row_list)
            
            name_csv_str = "PackageMasterCSV" +datetime.now().strftime("%Y%m%d_%H%M%S")

            with open("media/" +  name_csv_str +'.csv', 'w', newline='',encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(package_csv_list)

            
            package_serializer = Package_Serializer(package_list, many=True)


            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "success"
            base_DTO_obj.massage = "seach package"
            base_DTO_obj.data_list = package_serializer.data
            base_DTO_obj.csv_name =  name_csv_str + '.csv'

            package_list_Serializer_DTO = Package_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(package_list_Serializer_DTO.data,safe=False)

        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = e
            base_DTO_obj.data = None

            package_Serializer_DTO_reponse = Package_Serializer_DTO(base_DTO_obj)

            return JsonResponse(package_Serializer_DTO_reponse.data, safe=False)



@api_view(['GET', 'POST', 'DELETE'])
def truck_list(request):
    
    if request.method == 'GET':
        try:
            truck_list = Truck.objects.all()
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
                base_DTO_obj.massage = "Truck License is required"
                base_DTO_obj.data = None

                truck_Serializer_DTO = Truck_Serializer_DTO(base_DTO_obj)

                return JsonResponse(truck_Serializer_DTO.data, status=status.HTTP_200_OK) 
            
            elif truck_data['province'] is None or truck_data['province'].strip() == "" :

                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = "Province is required"
                base_DTO_obj.data = None

                truck_Serializer_DTO = Truck_Serializer_DTO(base_DTO_obj)

                return JsonResponse(truck_Serializer_DTO.data, status=status.HTTP_200_OK) 
            
            elif truck_data['truck_type'] is None or truck_data['truck_type'].strip() == "" :

                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = "Truck Type is required"
                base_DTO_obj.data = None

                truck_Serializer_DTO = Truck_Serializer_DTO(base_DTO_obj)

                return JsonResponse(truck_Serializer_DTO.data, status=status.HTTP_200_OK) 
            
            
            elif truck_data['fuel_type'] is None or truck_data['fuel_type'].strip() == "" :

                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = "Fuel Type is required"
                base_DTO_obj.data = None

                truck_Serializer_DTO = Truck_Serializer_DTO(base_DTO_obj)

                return JsonResponse(truck_Serializer_DTO.data, status=status.HTTP_200_OK)
            
            elif truck_data['max_speed'] is None or truck_data['max_speed'] == "" :

                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = "Max Speed is required"
                base_DTO_obj.data = None

                truck_Serializer_DTO = Truck_Serializer_DTO(base_DTO_obj)

                return JsonResponse(truck_Serializer_DTO.data, status=status.HTTP_200_OK)
            
            elif truck_data['max_volume'] is None or truck_data['max_volume'] == "" :

                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = "Max Volume is required"
                base_DTO_obj.data = None

                truck_Serializer_DTO = Truck_Serializer_DTO(base_DTO_obj)

                return JsonResponse(truck_Serializer_DTO.data, status=status.HTTP_200_OK)
            
            elif truck_data['max_weight'] is None or truck_data['max_weight'] == "" :

                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = "Max Weight is required"
                base_DTO_obj.data = None

                truck_Serializer_DTO = Truck_Serializer_DTO(base_DTO_obj)

                return JsonResponse(truck_Serializer_DTO.data, status=status.HTTP_200_OK)
            
            else : 

                truck_list = Truck.objects.filter(truck_license = truck_data['truck_license'])
            
         
                if len(truck_list) >0 :

                    if truck_list[0].is_active :

                        base_DTO_obj =  base_DTO()
                        base_DTO_obj.serviceStatus = "Error"
                        base_DTO_obj.massage = "Truck License is duplicated"
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
                        base_DTO_obj.massage = "Truck Saved successfully"
                        base_DTO_obj.data = None

                        truck_Serializer_DTO_reponse = Truck_Serializer_DTO(base_DTO_obj)

                        return JsonResponse(truck_Serializer_DTO_reponse.data, status=status.HTTP_200_OK)

                truck_serializer_obj = Truck_Serializer(data=truck_data)
            
                if truck_serializer_obj.is_valid():

                    truck_serializer_obj.save()

                    base_DTO_obj =  base_DTO()
                    base_DTO_obj.serviceStatus = "success"
                    base_DTO_obj.massage = "Truck Saved successfully"
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
            base_DTO_obj.massage = "Truck Deleted successfully"
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
                base_DTO_obj.massage = "Province is required"
                base_DTO_obj.data = None

                truck_Serializer_DTO = Truck_Serializer_DTO(base_DTO_obj)

                return JsonResponse(truck_Serializer_DTO.data, status=status.HTTP_200_OK) 
            
            elif truck_data['truck_type'] is None or truck_data['truck_type'].strip() == "" :

                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = "Truck Type is required"
                base_DTO_obj.data = None

                truck_Serializer_DTO = Truck_Serializer_DTO(base_DTO_obj)

                return JsonResponse(truck_Serializer_DTO.data, status=status.HTTP_200_OK) 
            
            
            elif truck_data['fuel_type'] is None or truck_data['fuel_type'].strip() == "" :

                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = "Fuel Type is required"
                base_DTO_obj.data = None

                truck_Serializer_DTO = Truck_Serializer_DTO(base_DTO_obj)

                return JsonResponse(truck_Serializer_DTO.data, status=status.HTTP_200_OK)
            
            elif truck_data['max_speed'] is None or truck_data['max_speed'] == "" :

                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = "Max Speed is required"
                base_DTO_obj.data = None

                truck_Serializer_DTO = Truck_Serializer_DTO(base_DTO_obj)

                return JsonResponse(truck_Serializer_DTO.data, status=status.HTTP_200_OK)
            
            elif truck_data['max_volume'] is None or truck_data['max_volume'] == "" :

                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = "Max Volume is required"
                base_DTO_obj.data = None

                truck_Serializer_DTO = Truck_Serializer_DTO(base_DTO_obj)

                return JsonResponse(truck_Serializer_DTO.data, status=status.HTTP_200_OK)
            
            elif truck_data['max_weight'] is None or truck_data['max_weight'] == "" :

                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = "Max Weight is required"
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
                    base_DTO_obj.massage = "Truck Edited successfully"
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
                        "Update Time Stamp",
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
            driver_list = Driver.objects.all()
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
                base_DTO_obj.massage = "Driver Data is required"
                base_DTO_obj.data = None

                driver_Serializer_DTO = Driver_Serializer_DTO(base_DTO_obj)

                return JsonResponse(driver_Serializer_DTO.data, status=status.HTTP_200_OK) 
            
            elif driver_data['name'] is None or driver_data['name'].strip() == "" :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = "Driver Name is required"
                base_DTO_obj.data = None

                driver_Serializer_DTO = Driver_Serializer_DTO(base_DTO_obj)

                return JsonResponse(driver_Serializer_DTO.data, status=status.HTTP_200_OK) 
            
            elif driver_data['tel'] is None or driver_data['tel'].strip() == "" :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = "Driver Tel is required"
                base_DTO_obj.data = None

                driver_Serializer_DTO = Driver_Serializer_DTO(base_DTO_obj)

                return JsonResponse(driver_Serializer_DTO.data, status=status.HTTP_200_OK) 
            
            else :
                 
                driver_list = Driver.objects.filter(driver_code = driver_data['driver_code'])
                
                if len(driver_list) >0 :

                    if driver_list[0].is_active :
                        base_DTO_obj =  base_DTO()
                        base_DTO_obj.serviceStatus = "Error"
                        base_DTO_obj.massage = "Driver Code duplicate"
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
                        base_DTO_obj.massage = "Driver Seved successfully"
                        base_DTO_obj.data = None

                        driver_Serializer_DTO_reponse = Driver_Serializer_DTO(base_DTO_obj)

                        return JsonResponse(driver_Serializer_DTO_reponse.data, status=status.HTTP_200_OK)

                driver_serializer_obj = Driver_Serializer(data=driver_data)

                if driver_serializer_obj.is_valid():
                    
                    driver_serializer_obj.save()
                    base_DTO_obj =  base_DTO()
                    base_DTO_obj.serviceStatus = "success"
                    base_DTO_obj.massage = "Driver Seved successfully"
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
            base_DTO_obj.massage = "Driver Deleted successfully"
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
                base_DTO_obj.massage = "Driver Data is required"
                base_DTO_obj.data = None

                driver_Serializer_DTO = Driver_Serializer_DTO(base_DTO_obj)

                return JsonResponse(driver_Serializer_DTO.data, status=status.HTTP_200_OK) 
            
            elif driver_data['name'] is None or driver_data['name'].strip() == "" :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = "Driver Name is required"
                base_DTO_obj.data = None

                driver_Serializer_DTO = Driver_Serializer_DTO(base_DTO_obj)

                return JsonResponse(driver_Serializer_DTO.data, status=status.HTTP_200_OK) 
            
            elif driver_data['tel'] is None or driver_data['tel'].strip() == "" :
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = "Driver Tel is required"
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
                    base_DTO_obj.massage = "Driver Edited successfully"
                    base_DTO_obj.data_list = Driver.objects.all()

                    driver_list_serializer_DTO_reponse = Driver_list_Serializer_DTO(base_DTO_obj)

                    return JsonResponse(driver_list_serializer_DTO_reponse.data, safe=False) 
                
        

        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = e
            base_DTO_obj.data = None

            print(e)

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
                        "Updated Timestamp"
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
                "Update Time"
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
                    base_DTO_obj.massage = router_master_serializer_obj.errors
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
            routerInfo_list = RouterInfo.objects.all()
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
                "Update Time"
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
            calendarMaster_list = CalendarMaster.objects.all()
            calendarMaster_serializer_obj = CalendarMaster_Serializer(calendarMaster_list, many=True)

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "success"
            base_DTO_obj.massage = "get calendar master"
            base_DTO_obj.data_list = calendarMaster_serializer_obj.data

            calendarMaster_list_Serializer_DTO_obj = CalendarMaster_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(calendarMaster_list_Serializer_DTO_obj.data, status=status.HTTP_200_OK)
        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "error"
            base_DTO_obj.massage = e 
            # base_DTO_obj.data_list = order_serializer.data

            calendarMaster_list_Serializer_DTO_obj = CalendarMaster_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(calendarMaster_list_Serializer_DTO_obj.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':


        try:
            calendarMaster_data = JSONParser().parse(request)
            calendarMaster_data['updated_by'] = request.user.username

            calendarMaster_serializer_obj = CalendarMaster_Serializer(data=calendarMaster_data)

            if calendarMaster_serializer_obj.is_valid():
                
                calendarMaster_serializer_obj.save()
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "success"
                base_DTO_obj.massage = configMessage.configs.get("CALENDAR_MASTER_ADD_MASSAGE_SUCCESSFUL").data
                base_DTO_obj.data = calendarMaster_serializer_obj.data

                calendarMaster_Serializer_DTO_reponse = CalendarMaster_Serializer_DTO(base_DTO_obj)

                return JsonResponse(calendarMaster_Serializer_DTO_reponse.data, status=status.HTTP_201_CREATED) 
            

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = calendarMaster_serializer_obj.errors
            base_DTO_obj.data = None

            calendarMaster_Serializer_DTO_reponse = CalendarMaster_Serializer_DTO(base_DTO_obj)

            return JsonResponse(calendarMaster_Serializer_DTO_reponse.data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = e
            base_DTO_obj.data = None

            calendarMaster_Serializer_DTO = CalendarMaster_Serializer_DTO(base_DTO_obj)

        return JsonResponse(calendarMaster_Serializer_DTO.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def search_calendarMaster(request):

    if request.method == 'POST':

        try:
            customer_code_selected = request.data['customer_code_selected']
            project_code_selected = request.data['project_code_selected']
            plant_code_selected = request.data['plant_code_selected']
            working_day_selected = request.data['working_day_selected']

            query = "select * from master_data_calendarmaster "

            joint_str = "" 
            where_str = " where 1 = 1  and master_data_calendarmaster.is_active = true  "


            if customer_code_selected is not None:

                joint_str = joint_str + " INNER JOIN master_data_station "
                joint_str = joint_str + " ON UPPER(master_data_station.station_code) = UPPER(master_data_calendarmaster.plant_code) "
                joint_str = joint_str + " INNER JOIN master_data_project "
                joint_str = joint_str + " ON UPPER(master_data_project.project_code) = UPPER(master_data_station.project_code) "
                joint_str = joint_str + " INNER JOIN master_data_customer "
                joint_str = joint_str + " ON UPPER(master_data_customer.customer_code) = UPPER(master_data_project.customer_code) "
                where_str = where_str + " and  UPPER(master_data_customer.customer_code) = '%s' " % customer_code_selected.upper()
                    
            if project_code_selected is not None and customer_code_selected is None :
                
                joint_str = joint_str + " INNER JOIN master_data_station "
                joint_str = joint_str + " ON UPPER(master_data_station.station_code) = UPPER(master_data_calendarmaster.plant_code) "
                joint_str = joint_str + " INNER JOIN master_data_project "
                joint_str = joint_str + " ON UPPER(master_data_project.project_code) = UPPER(master_data_station.project_code) "
                where_str = where_str + " and  UPPER(master_data_project.project_code) = '%s' " % project_code_selected.upper()
            
            if project_code_selected is not None and customer_code_selected is not None :
               
                where_str = where_str + " and  UPPER(master_data_project.project_code) = '%s' " % project_code_selected.upper()

            if plant_code_selected is not None:

                where_str = where_str + " and  UPPER(master_data_calendarmaster.plant_code) = '%s' " % plant_code_selected.upper()
            
            if working_day_selected is not None:

                where_str = where_str + " and  master_data_calendarmaster.is_working = '%s' " % working_day_selected
            
            query = query + joint_str + where_str + "order by master_data_calendarmaster.date"

            print(query)

            calendarMaster_list = CalendarMaster.objects.raw(query)

            calendarMaster_csv_list = []

            calendarMaster_csv_list.insert(0, [
                "Plant",
                "Day",
                "Date",
                "Working Day",
                "Remark",
                "Update by",
                "Update Time"
                ]
            )

            calendarMaster_dto_list = []
            for calendarMaster_obj in calendarMaster_list:

                calendarMaster_row_list = (
                                calendarMaster_obj.plant_code,
                                covert_to_date_str(calendarMaster_obj.day),
                                calendarMaster_obj.date,
                                "Yes" if calendarMaster_obj.is_working  else "No",
                                calendarMaster_obj.remark,
                                calendarMaster_obj.updated_by,
                                calendarMaster_obj.updated_date.strftime("%d/%m/%Y")
                                )

                calendarMaster_csv_list.append(calendarMaster_row_list)

            name_csv_str = "CalendarMasterCSV_" +datetime.now().strftime("%Y%m%d_%H%M%S")

            with open("media/" +  name_csv_str +'.csv', 'w', newline='',encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(calendarMaster_csv_list)

            calendarMaster_serializer = CalendarMaster_Serializer(calendarMaster_list, many=True)

            
            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "success"
            base_DTO_obj.massage = "get calendarMaster"
            base_DTO_obj.data_list = calendarMaster_serializer.data
            base_DTO_obj.csv_name =  name_csv_str + '.csv'

            calendarMaster_list_Serializer_DTO = CalendarMaster_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(calendarMaster_list_Serializer_DTO.data, safe=False)

        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = e
            base_DTO_obj.data = None

            calendarMaster_list_Serializer_DTO = CalendarMaster_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(calendarMaster_list_Serializer_DTO.data, safe=False)

def covert_to_date_str(date_int):

    if date_int == 1 :

        return "อาทิตย์"
    
    if date_int == 2 :

        return "จันทร์"
    
    if date_int == 3 :

        return "อังคาร"
    
    if date_int == 4 :

        return "พุธ"
    
    if date_int == 5 :

        return "พฤหัสบดี"
    
    if date_int == 6 :

        return "ศุกร์"

    if date_int == 7 :

        return "เสาร์ "
    


@api_view(['GET', 'POST', 'DELETE'])
def edited_calendarMaster(request):

    if request.method == 'POST':

        try:

            calendarMaster_data = JSONParser().parse(request)
            calendarMaster_obj = CalendarMaster.objects.get( id = calendarMaster_data['id'] )
            

            if calendarMaster_data['is_working'] is None or calendarMaster_data['is_working'] == "":

                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = configMessage.configs.get("CALENDAR_MASTER_WORKING_REQUIRED").data
                base_DTO_obj.data_list = CalendarMaster.objects.all()

                calendarMaster_list_serializer_DTO_reponse = CalendarMaster_list_Serializer_DTO(base_DTO_obj)

                return JsonResponse(calendarMaster_list_serializer_DTO_reponse.data, safe=False) 
            
            calendarMaster_data["date"] = datetime.strptime(calendarMaster_data["date"] , "%Y-%m-%d").strftime("%d-%m-%Y")

            calendarMaster_serializer_obj =  CalendarMaster_Serializer(calendarMaster_obj,data=calendarMaster_data)

            if calendarMaster_serializer_obj.is_valid():

                calendarMaster_serializer_obj.save()
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "success"
                base_DTO_obj.massage = configMessage.configs.get("CALENDAR_MASTER_EDIT_MASSAGE_SUCCESSFUL").data
                base_DTO_obj.data_list = CalendarMaster.objects.all()

                calendarMaster_list_serializer_DTO_reponse = CalendarMaster_list_Serializer_DTO(base_DTO_obj)

                return JsonResponse(calendarMaster_list_serializer_DTO_reponse.data, safe=False) 
            
            else : 
                
                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "Error"
                base_DTO_obj.massage = calendarMaster_serializer_obj.errors
                base_DTO_obj.data_list = CalendarMaster.objects.all()

                calendarMaster_list_serializer_DTO_reponse = CalendarMaster_list_Serializer_DTO(base_DTO_obj)

                return JsonResponse(calendarMaster_list_serializer_DTO_reponse.data, safe=False) 
            
        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = e
            base_DTO_obj.data = None

            calendarMaster_Serializer_DTO_reponse = CalendarMaster_Serializer_DTO(base_DTO_obj)

            return JsonResponse(calendarMaster_Serializer_DTO_reponse.data, safe=False)

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


