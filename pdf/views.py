  
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


truckPlanManagementService = TruckPlanManagementService()


serializerMapping = SerializerMapping() 

def generate_pdf(request):
    html = '<html><body><p>To PDF or not to PDF</p></body></html>'
    write_to_file = open('media/test.pdf', "w+b")
    result = pisa.CreatePDF(html,dest=write_to_file)
    write_to_file.close()
    return HttpResponse(result.err)


def generate_pdf_through_template(request):
    context={}

    number = '5901234123457'
    my_code = EAN13(number, writer=ImageWriter())
    my_code.save("new_code1")

    html = render_to_string('pdf/pdf_template.html',context)
    
    write_to_file = open('media/test_1.pdf', "w+b")
    
    result = pisa.CreatePDF(html,dest=write_to_file)
    
    write_to_file.close()
    
    return HttpResponse(result.err)

# def render_pdf(request):
#     path = "pdf/pdf_template.html"
#     person={}
#     person['state_id']=1
#     person['state_name']="makky"
#     person['thai']='male'
#     person['is_deleted']=False
#     context = {"states" : [person]}

#     html = render_to_string('pdf/pdf_template.html',context)
#     io_bytes = BytesIO()
    
#     pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), io_bytes)
    
#     if not pdf.err:
#         return HttpResponse(io_bytes.getvalue(), content_type='application/pdf')
#     else:
#         return HttpResponse("Error while rendering PDF", status=400)

def link_callback(uri, rel):
            """
            Convert HTML URIs to absolute system paths so xhtml2pdf can access those
            resources
            """
            result = finders.find(uri)
            if result:
                    if not isinstance(result, (list, tuple)):
                            result = [result]
                    result = list(os.path.realpath(path) for path in result)
                    path=result[0]
            else:
                    sUrl = settings.STATIC_URL        # Typically /static/
                    sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
                    mUrl = settings.MEDIA_URL         # Typically /media/
                    mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

                    if uri.startswith(mUrl):
                            path = os.path.join(mRoot, uri.replace(mUrl, ""))
                    elif uri.startswith(sUrl):
                            path = os.path.join(sRoot, uri.replace(sUrl, ""))
                    else:
                            return uri

            # make sure that file exists
            if not os.path.isfile(path):
                    raise Exception(
                            'media URI must start with %s or %s' % (sUrl, mUrl)
                    )
            return path

# @api_view(['POST'])
# def render_pickup_pdf(request):

#         path = "pdf/pdf_template.html"
#     person={}
#     person['state_id']=1
#     person['state_name']="makky"
#     person['thai']='male'
#     person['is_deleted']=False
#     context = {"states" : [person]}

#     html = render_to_string('pdf/pdf_template.html',context)
#     io_bytes = BytesIO()
    
#     pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), io_bytes)
    
#     if not pdf.err:
#         return HttpResponse(io_bytes.getvalue(), content_type='application/pdf')
#     else:
#         return HttpResponse("Error while rendering PDF", status=400)

@api_view(['POST'])
def render_pickup_pdf(request):

    if request.method == 'POST':

        try:
       
                pickup_data = JSONParser().parse(request)
                #name of pic barcode
                name_barcode_img_str = "barcode_" +datetime.now().strftime("%Y%m%d_%H%M%S") 
                barcode = Barcode(name_barcode_img_str)
                barcode.generate_code128(name_barcode_img_str)
                #get data for report
                data_list = truckPlanManagementService.pickup_report(pickup_data['pickup_no'])

                context = {"pickup_obj" :data_list[0][0],"order_list":data_list[1],"barcode_pic_name" :name_barcode_img_str}
                
                
                name_pdf_str = "PickupPDFCSV_" +datetime.now().strftime("%Y%m%d_%H%M%S") + ".pdf"

                html = render_to_string('pdf/pickup_template.html',context)

                print(html)
                write_to_file = open('media/'+name_pdf_str, "w+b")
                io_bytes = BytesIO()
                result = StringIO()
                print(StringIO(str(html.encode('utf-8'))))
                result = pisa.CreatePDF(html.encode('utf-8'),dest=write_to_file,link_callback=link_callback,encoding='utf-8-sig', html_encoding="utf-8-sig")
                
                write_to_file.close()

                PDF_serializer_DTO = serializerMapping.mapping_pdf(PDF_Serializer_DTO,'success','test',name_pdf_str)
                
                

                return JsonResponse(PDF_serializer_DTO.data, status=status.HTTP_200_OK)
                
                # if not pdf.err:
                #         return HttpResponse(io_bytes.getvalue(), content_type='application/pdf')
                # else:
                #         return HttpResponse("Error while rendering PDF", status=400)
        
        except Exception as e:

                PDF_serializer_DTO = serializerMapping.mapping_pdf(PDF_Serializer_DTO,'Error',e,'sadasdasd')

                return JsonResponse(PDF_serializer_DTO.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def render_pickup_pdf(request):

    if request.method == 'POST':

        try:
       
                pickup_data = JSONParser().parse(request)
                name_barcode_img_str = "barcode_" +datetime.now().strftime("%Y%m%d_%H%M%S") 
                barcode = Barcode(name_barcode_img_str)
                barcode.generate_code128(pickup_data['pickup_no'])

                data_list = truckPlanManagementService.pickup_report(pickup_data['pickup_no'])

                context = {"pickup_obj" :data_list[0][0],"order_list":data_list[1],"barcode_pic_name" :name_barcode_img_str}
                name_pdf_str = "PickupPDFCSV_" +datetime.now().strftime("%Y%m%d_%H%M%S") + ".pdf"
                html = render_to_string('pdf/pickup_template.html',context)
                PDFManagement.generate_pdf(html,name_pdf_str,link_callback)
  
                PDF_serializer_DTO = serializerMapping.mapping_pdf(PDF_Serializer_DTO,'success','test',name_pdf_str)
                
                return JsonResponse(PDF_serializer_DTO.data, status=status.HTTP_200_OK)

        except Exception as e:

                PDF_serializer_DTO = serializerMapping.mapping_pdf(PDF_Serializer_DTO,'Error',e,'sadasdasd')

                return JsonResponse(PDF_serializer_DTO.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def render_truckplan_pdf(request):

    if request.method == 'POST':

        try:
       
                truckplan_data = JSONParser().parse(request)
                name_barcode_img_str = "barcode_" +datetime.now().strftime("%Y%m%d_%H%M%S") 
                barcode = Barcode(name_barcode_img_str)
                barcode.generate_code128(truckplan_data['truckplan_no'])

                data_list = truckPlanManagementService.truck_report(truckplan_data['truckplan_no'])
                print(data_list)

                context = {"pickup_obj" :data_list[0][0],"order_list":data_list[1],"barcode_pic_name" :name_barcode_img_str}
                name_pdf_str = "TruckPlanPDF_" +datetime.now().strftime("%Y%m%d_%H%M%S") + ".pdf"
                html = render_to_string('pdf/truckPlan_template.html',context)
                PDFManagement.generate_pdf(html,name_pdf_str,link_callback)
  
                PDF_serializer_DTO = serializerMapping.mapping_pdf(PDF_Serializer_DTO,'success','test',name_pdf_str)
                
                return JsonResponse(PDF_serializer_DTO.data, status=status.HTTP_200_OK)

        except Exception as e:

                PDF_serializer_DTO = serializerMapping.mapping_pdf(PDF_Serializer_DTO,'Error',e,'sadasdasd')

                return JsonResponse(PDF_serializer_DTO.data, status=status.HTTP_200_OK)