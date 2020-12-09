  
from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from rest_framework import status
from django.template.loader import render_to_string
from io import BytesIO
from xhtml2pdf import pisa
from order.models import Order
from pdf.serializers import PDF_Serializer_DTO
from rest_framework.decorators import api_view,permission_classes
from app.serializersMapping.SerializerMapping import SerializerMapping
from rest_framework.parsers import JSONParser 
from datetime import datetime
from order.serializers import OrderSerializer
from master_data.models import Part,Package
from app.helper.barcode.Barcode import Barcode
from app.services.truck_plan_management.TruckPlanManagementService import TruckPlanManagementService
from io import StringIO
from app.helper.pdf_management.PDFManagement import PDFManagement
import os
from django.conf import settings
from django.template.loader import get_template
from django.contrib.staticfiles import finders
from app.helper.config.ConfigPart import ConfigPart
from app.helper.file_management.FileManagement import FileManagement

configPart = ConfigPart()

truckPlanManagementService = TruckPlanManagementService()


serializerMapping = SerializerMapping() 


def link_callback(uri, rel):

    return settings.MEDIA_ROOT+"\\"+ uri


@api_view(['POST'])
def render_pickup_pdf(request):

    if request.method == 'POST':

        try:
       
                pickup_data = JSONParser().parse(request)

                PDF_part_str = FileManagement.validate_folder(configPart.configs.get("PDF_TRUCKMANAGEMENT_PART").data)
                PDF_part_str =   PDF_part_str + "/"

                name_barcode_img_str = "barcode_" +datetime.now().strftime("%Y%m%d_%H%M%S") 
                barcode = Barcode(name_barcode_img_str)
                barcode.generate_code128(settings.MEDIA_ROOT+"\\"+PDF_part_str,pickup_data['pickup_no'])

                data_list = truckPlanManagementService.pickup_report(pickup_data['pickup_no'])

                context = {"pickup_obj" :data_list[0][0],"order_list":data_list[1],"barcode_pic_name" :PDF_part_str+name_barcode_img_str}
                name_pdf_str = "PickupPDFCSV_" +datetime.now().strftime("%Y%m%d_%H%M%S") + ".pdf"
                html = render_to_string('pdf/pickup_template.html',context)
                PDFManagement.generate_pdf(html,settings.MEDIA_ROOT+"\\"+PDF_part_str+ name_pdf_str,link_callback)
  
                PDF_serializer_DTO = serializerMapping.mapping_pdf(PDF_Serializer_DTO,'success','test',PDF_part_str+ name_pdf_str)
                
                return JsonResponse(PDF_serializer_DTO.data, status=status.HTTP_200_OK)

        except Exception as e:

                PDF_serializer_DTO = serializerMapping.mapping_pdf(PDF_Serializer_DTO,'Error',e,'sadasdasd')

                return JsonResponse(PDF_serializer_DTO.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def render_truckplan_pdf(request):

    if request.method == 'POST':

        try:
       
                truckplan_data = JSONParser().parse(request)

                PDF_part_str = FileManagement.validate_folder(configPart.configs.get("PDF_TRUCKMANAGEMENT_PART").data)
                PDF_part_str =   PDF_part_str + "/"
                name_barcode_img_str = "barcode_" +datetime.now().strftime("%Y%m%d_%H%M%S") 
                barcode = Barcode(name_barcode_img_str)
                barcode.generate_code128(settings.MEDIA_ROOT+"\\"+PDF_part_str,truckplan_data['truckplan_no'])

                data_list = truckPlanManagementService.truck_report(truckplan_data['truckplan_no'])
          
                context = {"pickup_obj" :data_list[0][0],"order_list":data_list[1],"barcode_pic_name" :PDF_part_str+name_barcode_img_str}
                name_pdf_str = "TruckPlanPDF_" +datetime.now().strftime("%Y%m%d_%H%M%S") + ".pdf"
                html = render_to_string('pdf/truckPlan_template.html',context)
                PDFManagement.generate_pdf(html,settings.MEDIA_ROOT+"\\"+PDF_part_str+ name_pdf_str,link_callback)
  
                PDF_serializer_DTO = serializerMapping.mapping_pdf(PDF_Serializer_DTO,'success','test',PDF_part_str+ name_pdf_str)
                
                return JsonResponse(PDF_serializer_DTO.data, status=status.HTTP_200_OK)

        except Exception as e:

                PDF_serializer_DTO = serializerMapping.mapping_pdf(PDF_Serializer_DTO,'Error',e,'sadasdasd')

                return JsonResponse(PDF_serializer_DTO.data, status=status.HTTP_200_OK)