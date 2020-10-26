from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from datetime import datetime
from django.utils import timezone
from master_data.models import Customer,Station
from model_DTO import responseDTO
from model_DTO.base_DTO import base_DTO
from order.models import File,Order
from uploads.models import File
from master_data.models import Part,Package,RouterMaster
import openpyxl 
import csv
import json
from django.views.decorators.csrf import csrf_exempt
from model_DTO.validateError import validateError,validateErrorList
from model_DTO.responseDTO import responseDTO
import os 
from .serializers import FileSerializer,File_Serializer_DTO,File_list_Serializer_DTO,validateErrorSerializer,validateErrorSerializerList,OrderSerializer,Order_list_Serializer_DTO,Order_transaction_Serializer,Order_transaction_Serializer_DTO,Order_transaction_list__Serializer_DTO
from rest_framework.permissions import IsAuthenticated
from annoying.functions import get_object_or_None
from django.db.models.expressions import RawSQL
from django.db.models import Q
import uuid
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes
from rest_framework.decorators import authentication_classes
import json
from .model.order_history import order_history
from .model.order_transaction import Order_transaction
from decimal import Decimal
from functools import reduce
import operator, random
from django.db.models.functions import Lower
import math
from openpyxl.utils import get_column_letter
from app.helper.config.ConfigMessage import ConfigMessage

configMessage = ConfigMessage()

class FileUploadView(APIView):
    parser_class = (FileUploadParser,)
    today_date_str = datetime.utcnow().strftime("%y%m%d")
    letter_list = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    validate_error_list = []
    order_csv_list = []
    order_csv_list_database = []
    order_list = []

    partNumber_list = []
    partDescription_list = []
    supplierName_list = []
    plantName_list = []
    due_date_list = []
        
    # authentication_classes =[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def generate_file_no(self,customer_id):

        today_date_str = self.today_date_str
        print(today_date_str)
        customer_code_str = Customer.objects.get(customer_code = customer_id ).customer_code
        customer_code_2dg_first_start_str = customer_code_str[0:2]

        file_count = File.objects.filter(file_no__contains= today_date_str ).count()
    
        file_count = file_count + 1
        if file_count < 10:
            file_count = "0" + str(file_count) 

        


        file_no = customer_code_2dg_first_start_str + today_date_str + str(file_count)

        return file_no

    def validated_cell(self,sheet_obj):

        row_max_int = sheet_obj.max_row
        column_max_int = sheet_obj.max_column

        validate_error_list = []

        for row_int in range(3, row_max_int + 1, 1):

            for column_int in range(1, column_max_int + 1, 1):
                
                order_cell_str = sheet_obj.cell(row=row_int, column=column_int).value
                is_error_bool = False

                if order_cell_str is not None :

                    if column_int > 5 :

                        due_date_str = sheet_obj.cell(row=2, column=column_int).value
                        due_date_obj = datetime.strptime(due_date_str.strftime("%d/%m/%Y"), "%d/%m/%Y")
                        # print(due_date_obj.year)
                        # print(due_date_obj.month)
                        # print(due_date_obj.day)
                        check_order_obj = Order.objects.filter(
                                part_number = sheet_obj.cell(row=row_int, column=2).value,
                                due_date__year = due_date_obj.year,
                                due_date__month = due_date_obj.month,
                                due_date__day = due_date_obj.day,
                                supplier_no = sheet_obj.cell(row=row_int, column=4).value,
                                plant_no = sheet_obj.cell(row=row_int, column=5).value

                            )
                        
                        if len(check_order_obj) > 0 :

                            order_row_list = (
                                        sheet_obj.cell(row=row_int, column=1).value,
                                        check_order_obj[0].order_id,
                                        sheet_obj.cell(row=row_int, column=2).value,
                                        sheet_obj.cell(row=row_int, column=3).value,
                                        sheet_obj.cell(row=row_int, column=4).value,
                                        sheet_obj.cell(row=row_int, column=5).value,
                                        order_cell_str,
                                        sheet_obj.cell(row=2, column=column_int).value.strftime("%d/%m/%Y")
                                    )
                            self.order_csv_list.append(order_row_list)
                    

                    # string = "geeks" 
                    # print(len(string))


                    if column_int == 1 and isinstance(order_cell_str, int) == False:

                        validate_error_obj = validateError()                         
                        validate_error_obj.error = "Item number must be numeric."
                        validate_error_obj.row = row_int
                        validate_error_obj.column = column_int                  
                                
                        validate_error_list.append(validate_error_obj)
                        is_error_bool = True

                    # if column_int == 4 and len(order_cell_str) > 6 :

                    #     validate_error_obj = validateError()                         
                    #     validate_error_obj.error = "Supplier Name must be Less than 6 letter"
                    #     validate_error_obj.row = row_int
                    #     validate_error_obj.column = column_int                             
                                
                    #     validate_error_list.append(validate_error_obj)
                    #     is_error_bool = True

                    station_list = Station.objects.filter( station_code = sheet_obj.cell(row=row_int, column=4).value,station_type = "SUPPLIER")
                    
                    if column_int == 4  and len(station_list) == 0:

                        validate_error_obj = validateError()                         
                        validate_error_obj.error = "Supplier code does not exist in database."
                        validate_error_obj.row = row_int
                        validate_error_obj.column = column_int                       
                                
                        validate_error_list.append(validate_error_obj)
                        is_error_bool = True
                    
                    plant_list = Station.objects.filter( station_code__iexact = sheet_obj.cell(row=row_int, column=5).value,station_type = "PLANT")
                    
                    if column_int ==  5  and len(plant_list) == 0:

                        validate_error_obj = validateError()                         
                        validate_error_obj.error = "Plant code does not exist in database."
                        validate_error_obj.row = row_int
                        validate_error_obj.column = column_int                       
                                
                        validate_error_list.append(validate_error_obj)
                        is_error_bool = True

                    if column_int == 5 and len(order_cell_str) > 10 :
                                
                        print(order_cell_str)
                        print(len(order_cell_str))
                        validate_error_obj = validateError()                         
                        validate_error_obj.error = "Plant must be Less than 6 letter"
                        validate_error_obj.row = row_int
                        validate_error_obj.column = column_int                       
                                
                        validate_error_list.append(validate_error_obj)
                        is_error_bool = True
                            
                    if column_int > 5 and isinstance(order_cell_str, int) == False :
                                
                        validate_error_obj = validateError()                         
                        validate_error_obj.error = "Quantity must be integer."
                        validate_error_obj.row = row_int
                        validate_error_obj.column = column_int
                        validate_error_list.append(validate_error_obj)
                        is_error_bool = True
                    
            

        return validate_error_list

    def get_order_csv_list(self,sheet_obj,file_no,username,customer_id,project_id):
        
        row_max_int = sheet_obj.max_row
        column_max_int = sheet_obj.max_column

        validate_error_list = []

       
        # self.order_csv_list.append([

        #         "Item No","Order ID","Part Number","Part Description","Supplier Code","Plant Code","Order Amount","Date"
        #     ])

        count_int = 1 

        for row_int in range(3, row_max_int + 1, 1):
                
            order_row_list = []


            for column_int in range(1, column_max_int + 1, 1):

                order_cell_str = sheet_obj.cell(row=row_int, column=column_int).value



                if column_int >= 6 and order_cell_str !=None:

                    due_date_str = sheet_obj.cell(row=2, column=column_int).value
                    due_date_obj = datetime.strptime(due_date_str.strftime("%d/%m/%Y"), "%d/%m/%Y")

                    check_order_obj = Order.objects.filter(
                            part_number = sheet_obj.cell(row=row_int, column=2).value,
                            due_date__year = due_date_obj.year,
                            due_date__month = due_date_obj.month,
                            due_date__day = due_date_obj.day,
                            supplier_no__iexact = str(sheet_obj.cell(row=row_int, column=4).value).upper(),
                            plant_no__iexact = str(sheet_obj.cell(row=row_int, column=5).value).upper()

                        )
                    
                    if len(check_order_obj) >0 and int(order_cell_str) != 0 and check_order_obj[0].order_qty != int(order_cell_str):

                        print("test1")
                        history_updated_obj = json.loads(check_order_obj[0].history_updated)
                        history_updated_obj['update'].append(check_order_obj[0].order_qty)

                        print(order_cell_str)
                        order_row_database_list = (
                            check_order_obj[0].item_no,
                            check_order_obj[0].part_number,
                            check_order_obj[0].file_id,
                            check_order_obj[0].order_id,
                            check_order_obj[0].due_date.strftime("%d/%m/%Y"),
                            order_cell_str,
                            check_order_obj[0].package_no,
                            check_order_obj[0].package_qty,
                            check_order_obj[0].route_trip,
                            json.dumps(history_updated_obj),
                            check_order_obj[0].supplier_no,
                            check_order_obj[0].plant_no, 
                            "True" if check_order_obj[0].is_route_completed  else "",
                            "True" if check_order_obj[0].is_part_completed  else "",
                            check_order_obj[0].project_code,
                            check_order_obj[0].created_by,
                            "True",
                            "",
                            sheet_obj.cell(row=row_int, column=3).value
                        )

                        # check_order_obj.update(order_qty = order_no_last_str,updated_by = username)


                        # order_csv_list.append(order_row_list)
                        self.order_csv_list_database.append(order_row_database_list)
                        
                    if len(check_order_obj) >0 and int(order_cell_str) == 0 :

                        print("test2")
                        history_updated_obj = json.loads(check_order_obj[0].history_updated)
                        history_updated_obj['delete'].append(check_order_obj[0].order_qty)
                        history_updated_json_str = json.dumps(history_updated_obj)


                        order_row_database_list = (
                            check_order_obj[0].item_no,
                            check_order_obj[0].part_number,
                            check_order_obj[0].file_id,
                            check_order_obj[0].order_id,
                            check_order_obj[0].due_date.strftime("%d/%m/%Y"),
                            check_order_obj[0].order_qty,
                            check_order_obj[0].package_no,
                            check_order_obj[0].package_qty,
                            check_order_obj[0].route_trip,
                            history_updated_json_str,
                            check_order_obj[0].supplier_no,
                            check_order_obj[0].plant_no, 
                            "True" if check_order_obj[0].is_route_completed  else "",
                            "True" if check_order_obj[0].is_part_completed  else "",
                            check_order_obj[0].project_code,
                            check_order_obj[0].created_by,
                            "",
                            "True" ,
                            sheet_obj.cell(row=row_int, column=3).value,


                        )

                        # check_order_obj.update(is_deleted = True,updated_by = username)

                        # order_csv_list.append(order_row_list)
                        self.order_csv_list_database.append(order_row_database_list)
                        
                    if len(check_order_obj) == 0 and int(order_cell_str) > 0 :
                        
                        print("test3")
                        due_date_str = sheet_obj.cell(row=2, column=column_int).value
                        due_date_str = due_date_str.strftime("%y%m%d")


                        order_obj_list = list(filter(lambda list: due_date_str in list[1], self.order_csv_list))

                        # if len(order_obj_list) == 0 :

                        #     order_obj_list = Order.objects.filter(order_id__contains= due_date_str ).order_by("-created_date")
                        
                        order_id_last_str = ""

                        if len(order_obj_list) > 0 :
                            order_no_last_str = order_obj_list[len(order_obj_list)-1][1]

                        else :

                            order_list = Order.objects.filter(order_id__contains= due_date_str ).order_by("-created_date")
                            
                            if len (order_list) > 0 :
    
                                order_no_last_str = order_list[0].order_id
                            else:
                                order_no_last_str = '0000000000'

                        order_no_last_str = self.generate_order_no(order_no_last_str,due_date_str)

                        order_add_obj = Order()

                        order_add_obj.file_id = file_no
                        order_add_obj.item_no = sheet_obj.cell(row=row_int, column=1).value
                        order_add_obj.order_id = order_no_last_str
                        order_add_obj.supplier_no = sheet_obj.cell(row=row_int, column=4).value
                        order_add_obj.plant_no = sheet_obj.cell(row=row_int, column=5).value
                        order_add_obj.part_number = sheet_obj.cell(row=row_int, column=2).value
                        order_add_obj.due_date = sheet_obj.cell(row=2, column=column_int).value
                        order_add_obj.order_qty = order_cell_str
                        order_add_obj.is_active = False,
                        order_add_obj.project_code = project_id

                        part_obj = Part.objects.filter(part_number=sheet_obj.cell(row=row_int, column=2).value,status=2,is_active=True)

                        if part_obj.exists():

                            order_add_obj.package_no = part_obj[0].package_no
                            
                            if part_obj[0].snp == 0 :

                                order_add_obj.package_qty = 00.00

                            else : 

                                order_add_obj.package_qty = order_add_obj.order_qty / part_obj[0].snp

                            order_add_obj.is_part_completed = True
                            
                        else:

                            order_add_obj.is_part_completed = False


                        router_obj = RouterMaster.objects.filter(   
                            supplier_code__iexact = sheet_obj.cell(row=row_int, column=4).value, 
                            plant_code__iexact = sheet_obj.cell(row=row_int, column=5).value,
                            is_active=True
                        )

                        if router_obj.exists():

                            order_add_obj.route_code = router_obj[0].route_code 
                            order_add_obj.route_trip = router_obj[0].route_code + "-" + router_obj[0].trip_no
                            order_add_obj.is_route_completed = True

                        else:

                            order_add_obj.is_route_completed = False

                        order_add_obj.created_by = username

                        order_row_list = (
                            order_add_obj.item_no,
                            order_add_obj.order_id,
                            order_add_obj.part_number,
                            sheet_obj.cell(row=row_int, column=3).value,
                            order_add_obj.supplier_no,
                            order_add_obj.plant_no,
                            order_add_obj.order_qty,
                            order_add_obj.due_date.strftime("%d/%m/%Y")
                        )

                        order_history_obj = order_history()
                        order_history_obj.add = order_add_obj.order_qty
                        order_history_obj.update = []
                        order_history_obj.delete = []
             
                        history_str = json.dumps( order_history_obj.__dict__ )

                        order_row_database_list = (
                            order_add_obj.item_no,
                            order_add_obj.part_number,
                            order_add_obj.file_id,
                            order_add_obj.order_id,
                            order_add_obj.due_date.strftime("%d/%m/%Y"),
                            order_add_obj.order_qty,
                            order_add_obj.package_no,
                            order_add_obj.package_qty,
                            order_add_obj.route_trip,
                            history_str,
                            order_add_obj.supplier_no,
                            order_add_obj.plant_no, 
                            "True" if order_add_obj.is_route_completed  else "",
                            "True" if order_add_obj.is_part_completed  else "",
                            order_add_obj.project_code,
                            order_add_obj.created_by, 
                            "",
                            "",
                            sheet_obj.cell(row=row_int, column=3).value

                        )
                        if len(self.order_csv_list) == 0 :

                            print("sdsd")
                            # order_obj_list = self.order_csv_list[0][1]

                        else : 
                       
                            order_obj_list = self.order_csv_list[len(self.order_csv_list)-1][1]

                        self.order_csv_list_database.append(order_row_database_list)
                        self.order_csv_list.append(order_row_list)

        return sorted(self.order_csv_list, key=lambda x: x[1])  

    def generate_order_no(self,amount,due_date_str):

        amount = amount + 1
        no_str = due_date_str 
        amount_letter_int = int(amount/1000)
        amount_minus_letter_int =  amount  % 1000 

        
        if amount_minus_letter_int == 0:

            no_str = no_str + self.letter_list[amount_letter_int ] + "001"
        
        else :

            order_number_str = str(amount)

            if amount > 1000 :

                amount_minus_letter_int = amount_minus_letter_int + 1

            if amount_minus_letter_int < 10:

                order_number_str = "00" + str(amount_minus_letter_int ) 

            elif amount_minus_letter_int < 100:

                order_number_str = "0" + str(amount_minus_letter_int )
            
            no_str = no_str + self.letter_list[amount_letter_int ] + order_number_str

        return no_str

        # no_strt = due_date_str

        # if order_no_last_str[0:6] == due_date_str :
        #     order_number_int = int(order_no_last_str[7:])

        #     if order_number_int == 999:
        #         letter_index_int = self.letter_list.index(order_no_last_str[6]) 
        #         no_strt = no_strt + self.letter_list[letter_index_int + 1] + "001"

        #     else :
        #         order_number_int = order_number_int + 1
        #         order_number_str = ""

        #         if order_number_int < 10:
        #             order_number_str = "00" + str(order_number_int) 
        #         elif order_number_int < 100:
        #             order_number_str = "0" + str(order_number_int)

        #         else :
        #             order_number_str = str(order_number_int)
                    

        #         no_strt = no_strt +order_no_last_str[6]+ order_number_str
        #         # print(no_strt)
        # else :

        #     no_strt = no_strt + "A001"

    def get_name_column_csv(self,number_col_int) :
        
        letter_str = ""
        letter_number_int = int(number_col_int % 24 )

        print(letter_number_int)
        if letter_number_int == 0:

            letter_str = letter_str + str(self.letter_list[23])

        else :

            letter_str = letter_str + str(self.letter_list[1-1])
            
        return letter_str 
    

    def get_order_data(self,sheet_obj):

        is_incorrect = False

        order_list = []
        
        self.partNumber_list = []
        self.partDescription_list = []
        self.supplierName_list = []
        self.plantName_list = []
        self.due_date_list = []

        

        for row_int in range(3,sheet_obj.max_row + 1):

            order_column = []

            for column_int in range(1,sheet_obj.max_column +1 ): 

                order_data_str =  sheet_obj.cell(row=row_int, column=column_int).value 
                
                if order_data_str != None or sheet_obj.cell(row=2, column=column_int).value != None:
                    
                    order_data_str ="" if order_data_str == None  else order_data_str

                    if column_int == 1 :
                        
                        order_list.append((str(order_data_str),row_int,column_int))
                    
                    if column_int == 2 :
                        self.partNumber_list.append(str(order_data_str))
                        order_list.append((str(order_data_str),row_int,column_int))
                    
                    elif column_int == 3 :

                        self.partDescription_list.append(str(order_data_str))
                        order_list.append((str(order_data_str),row_int,column_int))
                    
                    elif column_int == 4 :

                        self.supplierName_list.append(str(order_data_str))
                        order_list.append((str(order_data_str),row_int,column_int))

                    elif column_int == 5 :

                        self.plantName_list.append(str(order_data_str))
                        order_list.append((str(order_data_str),row_int,column_int))
                        # order_list.append((str(order_data_str),row_int,column_int,(
                        #     sheet_obj.cell(row=row_int, column=2).value,
                        #     sheet_obj.cell(row=row_int, column=4).value,
                        #     sheet_obj.cell(row=row_int, column=5).value,
                        #     due_date_datetime.year,
                        #     due_date_datetime.month,
                        #     due_date_datetime.day
                        #     )))
                    
                    ############################################################3
                    elif column_int > 5 :

                            due_date_datetime = sheet_obj.cell(row=2, column=column_int).value
                            if not due_date_datetime in [ d[0] for d in  self.due_date_list] :

                                due_date_db_list = Order.objects.filter(
                                    due_date__year= due_date_datetime.year,
                                    due_date__month=due_date_datetime.month,
                                    due_date__day=due_date_datetime.day,
                                    ).values_list("due_date__day")

                                self.due_date_list.append((due_date_datetime,len(due_date_db_list)) )

                            order_list.append((str(order_data_str),row_int,column_int,(
                                str(sheet_obj.cell(row=row_int, column=2).value) if str(sheet_obj.cell(row=row_int, column=2).value).isnumeric() else str(sheet_obj.cell(row=row_int, column=2).value).upper(),
                                str(sheet_obj.cell(row=row_int, column=4).value) if str(sheet_obj.cell(row=row_int, column=4).value).isnumeric() else str(sheet_obj.cell(row=row_int, column=4).value).upper(),
                                str(sheet_obj.cell(row=row_int, column=5).value) if str(sheet_obj.cell(row=row_int, column=5).value).isnumeric() else str(sheet_obj.cell(row=row_int, column=5).value).upper(),
                                due_date_datetime.year,
                                due_date_datetime.month,
                                due_date_datetime.day
                                ),
                                (
                                    str(sheet_obj.cell(row=row_int, column=1).value),
                                    str(sheet_obj.cell(row=row_int, column=2).value),
                                    str(sheet_obj.cell(row=row_int, column=3).value),
                                    str(sheet_obj.cell(row=row_int, column=4).value),
                                    str(sheet_obj.cell(row=row_int, column=5).value),
                                    due_date_datetime
                                )
                                ))
        
        return order_list

    def post(self, request, *args, **kwargs):

        try:
            file_serializer = FileSerializer(data=request.data)
            customer_id = request.POST.get("customer_id", "")
            project_id = request.POST.get("project_id", "")

            self.order_csv_list_database = []
            self.order_csv_list = []
            
            if file_serializer.is_valid():

                file_no = self.generate_file_no(request.POST.get("customer_id", ""))

                file_serializer.save(file_no = file_no , 
                    file_name = request.FILES['file'].name ,
                    file_size = request.FILES['file'].size,
                    customer_id = customer_id,
                    project_id = project_id,
                    status = 1,
                    created_by = request.user.username,
                    created_date = datetime.now(tz=timezone.utc)
                    )
                
                workbook_obj = openpyxl.load_workbook(file_serializer.data['file'][1:])
                sheet_obj = workbook_obj.active

                row_max_int = sheet_obj.max_row
                column_max_int = sheet_obj.max_column

                order_list = self.get_order_data(sheet_obj)

                supplier_db_list = set(Station.objects.filter(station_code__iregex=r'(' + '|'.join(self.supplierName_list) + ')',station_type__iexact="SUPPLIER",is_active=True).values_list("station_code",flat=True))
                supplier_db_set = set([s.upper() for s in supplier_db_list])
                supplier_excel_set = set([s.upper() for s in self.supplierName_list])
                not_supplier_in_db = set(supplier_excel_set - supplier_db_set)
                
                plant_db_list = Station.objects.filter(station_code__iregex=r'(' + '|'.join(self.plantName_list) + ')',station_type__iexact="PLANT",is_active=True).values_list("station_code",flat=True)
                plant_db_set = set([p.upper() for p in plant_db_list])
                plant_excel_set = set([p.upper() for p in self.plantName_list])
                not_plant_in_db = set(plant_excel_set - plant_db_set)

                
                # order_missing_plant_list = [ x for x in order_list if x[1] in list(order_plant_list) and x[2] > 5]
                item_list = [ x for x in order_list if x[2] == 1 and (not x[0].isnumeric() or x[0] == "") ]
                partNumber_list = [ x for x in order_list if x[2] == 2 and x[0] == "" ]
                partDescription_list = [ x for x in order_list if x[2] == 3 and x[0] == "" ]
                order_supplier_list = [ x for x in order_list if x[0].upper() in list(not_supplier_in_db) and x[2] == 4 ]
                order_plant_list = [ x for x in order_list if x[0].upper()  in list(not_plant_in_db) and x[2] == 5 ]
                order_qry_list = [ x for x in order_list if x[2] > 5 and not x[0].isnumeric() ]

                validate_excel_error_list =  item_list+partNumber_list +partDescription_list + order_supplier_list + order_plant_list + order_qry_list
                
                if len(validate_excel_error_list) >0 :

                    validate_error_list = []
                    file_deleted_obj = File.objects.filter(created_by= request.user.username, status = 1)[0]
                    file_deleted_obj.delete()

                    for error in validate_excel_error_list:

                        validate_error_obj = validateError() 
                        if error[2] == 1:
                            
                            if error[0] is None or error[0] == "" :

                                validate_error_obj.error = configMessage.configs.get("UPLOAD_ORDER_ITEM_REQUIRED").data
                                validate_error_obj.row = error[1]
                                validate_error_obj.column = get_column_letter(error[2])
                            
                            elif not error[0].isnumeric() :

                                validate_error_obj.error = configMessage.configs.get("UPLOAD_ORDER_ITEM_INTEGER").data
                                validate_error_obj.row = error[1]
                                validate_error_obj.column = get_column_letter(error[2])
                        
                        if error[2] == 2:
                            
                            if error[0] is None or error[0] == "" :

                                validate_error_obj.error = configMessage.configs.get("UPLOAD_ORDER_PARTNUMBER_REQUIRED").data
                                validate_error_obj.row = error[1]
                                validate_error_obj.column = get_column_letter(error[2])
                        
                        if error[2] == 3:
                            
                            if error[0] is None or error[0] == "" :

                                validate_error_obj.error = configMessage.configs.get("UPLOAD_ORDER_PARTDESCRIPTION_REQUIRED").data
                                validate_error_obj.row = error[1]
                                validate_error_obj.column = get_column_letter(error[2])

                        if error[2] == 4:

                            station_len_int = len(Station.objects.filter(station_code__iexact= str(error[0]) ,station_type__iexact="PLANT",is_active=True))
           
                            if error[0] is None or error[0] == "" :

                                validate_error_obj.error = configMessage.configs.get("UPLOAD_ORDER_SUPPLIERCODE_REQUIRED").data
                                validate_error_obj.row = error[1]
                                validate_error_obj.column = get_column_letter(error[2])

                            elif station_len_int == 0 :
    
                                validate_error_obj.error = configMessage.configs.get("UPLOAD_ORDER_SUPPLIERCODE_DATABASE").data
                                validate_error_obj.row = error[1]
                                validate_error_obj.column = get_column_letter(error[2]) 

                        # check plant code 
                        elif error[2] == 5 :
                            
                            station_len_int = len(Station.objects.filter(station_code__iexact= str(error[0]),station_type__iexact="PLANT",is_active=True))
                            
                            if error[0] is None or error[0] == "" :

                                validate_error_obj.error = configMessage.configs.get("UPLOAD_ORDER_PLANTCODE_REQUIRED").data
                                validate_error_obj.row = error[1]
                                validate_error_obj.column = get_column_letter(error[2])
                            
                            elif station_len_int == 0 :
                                validate_error_obj.error = configMessage.configs.get("UPLOAD_ORDER_PLANTCODE_DATABASE").data
                                validate_error_obj.row = error[1]
                                validate_error_obj.column = get_column_letter(error[2]) 
                        
                        elif error[2] > 5 :

                            if error[0] is None or error[0] == "" :

                                validate_error_obj.error = configMessage.configs.get("UPLOAD_ORDER_QUANTITY_REQUIRED").data
                                validate_error_obj.row = error[1]
                                validate_error_obj.column = get_column_letter(error[2])

                            elif not error[0].isnumeric() :

                                validate_error_obj.error = configMessage.configs.get("UPLOAD_ORDER_QUANTITY_INTEGER").data
                                validate_error_obj.row = error[1]
                                validate_error_obj.column = get_column_letter(error[2])
                        
                        
                        validate_error_list.append(validate_error_obj)

                    #####################################################
                    validateErrorListObj =  validateErrorList()
                    validateErrorListObj.serviceStatus = "Error"
                    validateErrorListObj.massage = configMessage.configs.get("UPLOAD_FILE_MASSAGE_ERROR").data
                    validateErrorListObj.validateErrorList = sorted(validate_error_list, key=lambda error: (error.row,error.column) )

                    serializer = validateErrorSerializerList(validateErrorListObj)
                    return Response(serializer.data, status=status.HTTP_200_OK)

                else :
                    
                    order_database_list = set(Order.objects.filter(is_deleted=False).values_list("part_number","supplier_no","plant_no","due_date__year","due_date__month","due_date__day","order_id","order_qty","history_updated"))
                    order_database_set = set([(p[0].upper(),p[1].upper(),p[2].upper(),p[3],p[4],p[5]) for p in order_database_list ])
                    order_excel_set = set([p[3] for p in order_list if p[2] > 5 and  str(p[0]).isnumeric() and int(str(p[0])) >0 ] )
                    

                    order_csv_list = []
                    order_csv_list_database = []
                    order_loop_list = [o for o in order_list if   (o[2] > 5 and int(o[0]) > 0 )]
                    
                    for  order_obj in order_loop_list :

                        order_history_obj = order_history()
                        
                        if  not order_obj[3] in order_database_set: 
                            
                            order_id = self.generate_order_no([d[1] for d in self.due_date_list if d[0] == order_obj[4][5]][0],order_obj[4][5].strftime("%Y%m%d"))
                            
                            order_history_obj.add = order_obj[0]
                            order_history_obj.update = []
                            order_history_obj.delete = []
             
                            history_str = json.dumps( order_history_obj.__dict__ )

                            order_row_database_obj = (
                                order_obj[4][0], #Item_no
                                order_obj[4][1], #part_number
                                file_no, #file_no
                                order_id, #order_id
                                order_obj[4][5].strftime("%d/%m/%Y"), #due_date 
                                order_obj[0], #order_qty
                                history_str, #history_str
                                order_obj[4][3], # supplier_no
                                order_obj[4][4], # plant_no
                                order_obj[4][2], # part_name,
                                "add"
                            )

                            order_row_list = (
                                order_obj[4][0],
                                order_id,
                                order_obj[4][1],
                                order_obj[0],
                                order_obj[4][3],
                                order_obj[4][4],
                                order_obj[0],
                                order_obj[4][5].strftime("%d/%m/%Y")
                            )
                            update =  [ idx for idx,  d in enumerate(self.due_date_list) if d[0] == order_obj[4][5]]
                            self.due_date_list[update[0]]  = (self.due_date_list[update[0]][0],self.due_date_list[update[0]][1] +1  )

                            order_csv_list_database.append(order_row_database_obj)
                            order_csv_list.append(order_row_list)

                        else :

                            order_in_db_list = [o for o in order_database_list if  {o[0].upper(),o[1].upper(),o[2].upper(),o[3],o[4],o[5]} == set(order_obj[3])  ]
         
                            if len(order_in_db_list) > 0 and int(order_in_db_list[0][7]) !=  int(order_obj[0]):

                                history_updated_obj = json.loads(order_in_db_list[0][8])
                                history_updated_obj['update'].append(order_in_db_list[0][7])
                                history_updated_json_str = json.dumps(history_updated_obj)

                                order_row_database_obj = (
                                    order_obj[4][0], #Item_no
                                    order_obj[4][1], #part_number
                                    file_no, #file_no
                                    order_in_db_list[0][6], #order_id
                                    order_obj[4][5].strftime("%d/%m/%Y"), #due_date 
                                    order_obj[0], #order_qty
                                    history_updated_json_str, #history_str
                                    order_obj[4][3], # supplier_no
                                    order_obj[4][4], # plant_no
                                    order_obj[4][2], # part_name,
                                    "update"
                                )
                                order_csv_list_database.append(order_row_database_obj)

                            order_row_list = (
                                order_obj[4][0],
                                order_in_db_list[0][6],
                                order_obj[4][1],
                                order_obj[0],
                                order_obj[4][3],
                                order_obj[4][4],
                                order_obj[0],
                                order_obj[4][5].strftime("%d/%m/%Y")
                            )
                        
                            
                            order_csv_list.append(order_row_list)

                    delete_order_list = [o for o in order_database_list if (o[0].upper(),o[1].upper(),o[2].upper(),o[3],o[4],o[5]) not in order_excel_set   ]
                    
                    for delete_order in delete_order_list :
                        print("delete")
                        history_updated_obj = json.loads(delete_order[8])
                        history_updated_obj['delete'].append(delete_order[7])
                        history_updated_json_str = json.dumps(history_updated_obj)

                        order_row_database_obj = (
                            "", #Item_no,
                            "", #part_number
                            "", #file_no
                            delete_order[6], #order_id
                            "", #due_date 
                            "", #order_qty
                            history_updated_json_str, #history_str
                            "", # supplier_no
                            "", # plant_no
                            "", # part_name,
                            "delete"
                            )
                        order_csv_list_database.append(order_row_database_obj)
                        
                        
                    file_list = File.objects.filter(file_no=file_no)
                    file_list.update(order_count= len(order_loop_list))
                    
                    order_csv_list = sorted(order_csv_list, key=lambda x: x[1])
                    
                    order_csv_list.insert(0, [
                            "Item No","Order ID",
                            "Part Number",
                            "Part Description",
                            "Supplier Name",
                            "Plant",
                            "Order Amount",
                            "Date"
                        ]
                    )
                    with open("media/" + file_no + '.csv', 'w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerows(order_csv_list)
                    
                    with open("media/" + file_no + '_database.csv', 'w', newline='') as file:
                        writer = csv.writer(file, delimiter=";", quotechar="'")
                        writer.writerows(order_csv_list_database)

                    validateErrorListObj =  validateErrorList()
                    validateErrorListObj.serviceStatus = "success"
                    validateErrorListObj.massage = configMessage.configs.get("UPLOAD_FILE_MASSAGE_SUCCESSFUL").data
                    validateErrorListObj.fileList = None

                    serializer = validateErrorSerializerList(validateErrorListObj)
                    return Response(serializer.data, status=status.HTTP_200_OK)
               
        except Exception as e:

            validateErrorListObj =  validateErrorList()
            validateErrorListObj.serviceStatus = "Error"
            validateErrorListObj.massage = e
            validateErrorListObj.fileList = None

            file_deleted_obj = File.objects.filter(created_by= request.user.username, status = 1)
            file_deleted_obj.delete()

            serializer = validateErrorSerializerList(validateErrorListObj)

            return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get(request):
    if request.method == 'GET':
        # print(request.user.username)
        file_list = File.objects.filter(created_by= request.user.username, status = 1)

        file_serializer = FileSerializer(file_list, many=True)

        return JsonResponse(file_serializer.data, safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def confirm(request):

    if request.method == 'GET':

        # File.objects.filter(created_by= request.user.username, status = False).update(status = True)
        try:
            file_comfirm_list = File.objects.filter(created_by= request.user.username, status = 1)
            file_no_str = file_comfirm_list[0].file_no
            

            part_list = Part.objects.filter(is_active=True)
            package_list = Package.objects.filter(is_active=True)
            routerMaster_list = RouterMaster.objects.filter(is_active=True)
            order_list = Order.objects.filter()
            with open("media/" + str(file_no_str) + "_database.csv", newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
                for row in spamreader:
                    

                    if row[10] == "add" :
                        
                        order_add_obj = Order()
                        order_add_obj.item_no = row[0]
                        order_add_obj.part_number = row[1]
                        order_add_obj.file_id = row[2]
                        order_add_obj.order_id = row[3]
                        order_add_obj.due_date = datetime.strptime(str(row[4]), "%d/%m/%Y")
                        order_add_obj.order_qty = int(row[5])
                        order_add_obj.history_updated = row[6]
                        order_add_obj.supplier_no = row[7]
                        order_add_obj.plant_no = row[8]

                        part_db_list = [p for p in part_list if p.part_number.upper() == row[1] and p.status==2 ]
                        
                        if len(part_db_list) > 0 :
                            
                            order_add_obj.is_part_completed = True

                            package_db_list = [p for p in package_list if p.package_no.upper() == part_db_list[0].package_no.upper() ]

                            if len(package_db_list) > 0 :
                                
                                order_add_obj.package_no = package_db_list[0].package_no
                                order_add_obj.package_qty = math.ceil(int(row[5])/package_db_list[0].snp)
                            
                        else :
                            
                            check_part_list  = Part.objects.filter(part_number=row[1])
                            
                            order_add_obj.is_part_completed = False

                            if len(check_part_list) == 0  :
                              
                                part = Part()
                                part.part_number  = row[1]
                                part.project_code = file_comfirm_list[0].project_id
                                part.supplier_code = row[7]
                                part.part_name = row[9]
                                part.package_no = None
                                part.updated_by = request.user.username
                                part.is_active = True
                                part.status = 1
                                
                                part.save()
                            

                        routerMaster_db_list = [r for r in routerMaster_list if r.supplier_code.upper() == row[7].upper() and r.plant_code.upper() == row[8].upper() ]

                        if len(routerMaster_db_list) > 0 :

                            order_add_obj.is_route_completed = True
                            order_add_obj.route_trip = routerMaster_db_list[0].route_no
                            order_add_obj.route_code = routerMaster_db_list[0].route_code
                            order_add_obj.trip_no = routerMaster_db_list[0].trip_no

                        else :

                            order_add_obj.is_route_completed = False
                        
                        order_add_obj.project_code = file_comfirm_list[0].project_id
                        order_add_obj.updated_by = request.user.username
                        order_add_obj.updated_date = datetime.utcnow()
                        order_add_obj.save()
                    
                    if row[10] == "update" :
                        
                        print(row[3])
                        order_update_obj= Order.objects.filter(order_id__iexact=row[3])
                        order_update_obj.update(
                            order_qty=int(row[5]),
                            history_updated=row[6],
                            updated_date=datetime.utcnow(),
                            updated_by=request.user.username,
                            is_deleted=False)
                    
                    if row[10] == "delete" :
                        
                        order_update_obj= Order.objects.filter(order_id__iexact=row[3])
                        order_update_obj.update(
                            history_updated=row[6],
                            updated_date=datetime.utcnow(),
                            updated_by=request.user.username,
                            is_deleted=True)
                  
            file_comfirm_list.update(status = 2)

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "success"
            base_DTO_obj.massage = configMessage.configs.get("UPLOAD_ORDER_MASSAGE_SUCCESSFUL").data
            base_DTO_obj.data = None
            file_serializer_DTO = File_Serializer_DTO(base_DTO_obj)
            return JsonResponse(file_serializer_DTO.data, safe=False)

        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = e
            base_DTO_obj.data = None
            file_serializer_DTO = File_Serializer_DTO(base_DTO_obj)

            return JsonResponse(file_serializer_DTO.data, safe=False)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def not_confirm(request):

    if request.method == 'POST':

        try:

            file_deleted_obj = File.objects.filter(created_by= request.user.username, status = 1)[0]
            file_no_str = file_deleted_obj.file_no
            file_file_str = file_deleted_obj.file

            order_deleted_obj = Order.objects.filter(file_id = file_no_str)

            file_deleted_obj.delete()
            order_deleted_obj.delete()
            
            os.remove("media/" + str(file_no_str) + ".csv")
            os.remove("media/" + str(file_no_str) + "_database.csv")
            os.remove("media/" + str(file_file_str))

    
            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "success"
            base_DTO_obj.massage = configMessage.configs.get("CANCEN_CONFIRM_ORDER_MASSAGE_SUCCESSFUL").data
            base_DTO_obj.data = None
            file_serializer_DTO = File_Serializer_DTO(base_DTO_obj)

            return JsonResponse(file_serializer_DTO.data, safe=False)

        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "error"
            base_DTO_obj.massage = e
            base_DTO_obj.data = None
            file_serializer_DTO = File_Serializer_DTO(base_DTO_obj)

            return JsonResponse(file_serializer_DTO.data, safe=False)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def search_miss_match(request):

    if request.method == 'POST':

        try:
            
            customer_selected = request.data['customer_selected']
            project_selected = request.data['project_selected']
            supplier_selected = request.data['supplier_selected']
            plant_selected = request.data['plant_selected']
            start_date_selected = request.data['start_date_selected']
            end_date_selected = request.data['end_date_selected']

            query = "select * from order_order "

            joint_str = "" 
            where_str = " where 1 = 1 and (order_order.is_part_completed = false or  order_order.is_route_completed = false) and order_order.is_deleted = false  "

            if customer_selected is not None:

                joint_str = joint_str + " INNER JOIN master_data_project "
                joint_str = joint_str + " ON master_data_project.project_code = order_order.project_code "
                joint_str = joint_str + " INNER JOIN master_data_customer "
                joint_str = joint_str + " ON master_data_customer.customer_code = master_data_project.customer_code "
                where_str = where_str + " and  UPPER(master_data_customer.customer_code) = '%s' " % customer_selected.upper()
            
            if customer_selected is not None and project_selected is not None:

                where_str = where_str + "and  UPPER(master_data_project.project_code) = '%s' " % project_selected.upper()
            
            if customer_selected is None and project_selected is not None:

                joint_str = joint_str + " INNER JOIN master_data_project "
                joint_str = joint_str + "ON master_data_project.project_code = order_order.project_code "
                where_str = where_str + "and  UPPER(master_data_project.project_code) = '%s' " % project_selected.upper()
            
            if supplier_selected is not None:

                where_str = where_str + "and  UPPER(order_order.supplier_no) = '%s' " % supplier_selected.upper()
            
            if plant_selected is not None:

                where_str = where_str + "and  UPPER(order_order.plant_no)  = '%s' " % plant_selected.upper()

            if start_date_selected is not None and end_date_selected is not None:

                start_date_str = datetime.strptime(start_date_selected, "%d/%m/%Y").strftime("%Y/%m/%d")
                end_date_str = datetime.strptime(end_date_selected, "%d/%m/%Y").strftime("%Y/%m/%d")

                where_str = where_str + "and due_date between '%s' and '%s'" % (start_date_str,end_date_str)

            query = query + joint_str + where_str + " order by order_order.order_id "

            order_list = Order.objects.raw(query)
            print(order_list)

            order_csv_list = []

            order_csv_list.insert(0, [
                        "File ID",
                        "Order ID",
                        "Supplier",
                        "Plant",
                        "Part No",
                        "Due Date",
                        "Order Qty",
                        "Pakage No",
                        "Pakage Qty",
                        "Route&Qty",
                        "Uploaded By",
                        "Uploaded Date",
                    ]
                )


            for order_obj in order_list:

                order_row_list = (
                    order_obj.file_id,
                    order_obj.order_id,
                    order_obj.supplier_no,
                    order_obj.plant_no,
                    order_obj.part_number,
                    order_obj.due_date.strftime("%d/%m/%Y"),
                    order_obj.order_qty,
                    order_obj.package_no,
                    "" if order_obj.package_no == None or order_obj.package_no == ""  else order_obj.package_qty,
                    "" if order_obj.route_code == None or order_obj.route_code == ""  else order_obj.route_code + "-" +order_obj.route_trip,
                    order_obj.updated_by,
                    order_obj.updated_date.strftime("%d/%m/%Y")

                    )
                
                order_csv_list.append(order_row_list)

            name_csv_str = str(uuid.uuid4())

            name_csv_str = "OrderMissMatchCSV_" +datetime.now().strftime("%Y%m%d_%H%M%S")

            with open("media/" +  name_csv_str +'.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(order_csv_list)

            order_serializer = OrderSerializer(order_list, many=True)

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "success"
            base_DTO_obj.massage = "get part"
            base_DTO_obj.data_list = order_serializer.data
            base_DTO_obj.csv_name =  name_csv_str + '.csv'

            order_list_Serializer_DTO = Order_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(order_list_Serializer_DTO.data,  safe=False)

        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = e
            base_DTO_obj.data_list = None

            print(e)

            order_list_Serializer_DTO = Order_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(order_list_Serializer_DTO.data,safe=False)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def search_pending_order(request):

    if request.method == 'POST':

        try:
            
            customer_selected = request.data['customer_selected']
            project_selected = request.data['project_selected']
            supplier_selected = request.data['supplier_selected']
            plant_selected = request.data['plant_selected']
            start_date_selected = request.data['start_date_selected']
            end_date_selected = request.data['end_date_selected']


            query = "select * from order_order "

            joint_str = "" 
            where_str = " where 1 = 1 and order_order.is_part_completed = true and  order_order.is_route_completed = true and order_order.is_deleted = false "

            if customer_selected is not None:

                joint_str = joint_str + " INNER JOIN master_data_project "
                joint_str = joint_str + " ON master_data_project.project_code = order_order.project_code "
                joint_str = joint_str + " INNER JOIN master_data_customer "
                joint_str = joint_str + " ON master_data_customer.customer_code = master_data_project.customer_code "
                where_str = where_str + " and  UPPER(master_data_customer.customer_code)  = '%s' " % customer_selected.upper()
            
            if customer_selected is not None and project_selected is not None:

                where_str = where_str + "and  UPPER(master_data_project.project_code) = '%s' " % project_selected.upper()
            
            if customer_selected is None and project_selected is not None:

                joint_str = joint_str + " INNER JOIN master_data_project "
                joint_str = joint_str + "ON master_data_project.project_code = order_order.project_code "
                where_str = where_str + "and  UPPER(master_data_project.project_code) = '%s' " % project_selected.upper()
            
            if supplier_selected is not None:

                where_str = where_str + "and  UPPER(order_order.supplier_no) = '%s' " % supplier_selected.upper()
            
            if plant_selected is not None:

                where_str = where_str + "and  UPPER(order_order.plant_no) = '%s' " % plant_selected.upper()

            if start_date_selected is not None and end_date_selected is not None:

                start_date_str = datetime.strptime(request.data['start_date_selected'], "%d/%m/%Y").strftime("%Y/%m/%d")
                end_date_str = datetime.strptime(request.data['end_date_selected'], "%d/%m/%Y").strftime("%Y/%m/%d")

                where_str = where_str + "and due_date between '%s' and '%s'" % (start_date_str,end_date_str)

            query = query + joint_str + where_str + " order by order_order.order_id "

            order_list = Order.objects.raw(query)

            print(query)

            order_csv_list = []

            order_csv_list.insert(0, [
                        "File ID",
                        "Order ID",
                        "Supplier",
                        "Plant",
                        "Part No",
                        "Due Date",
                        "Order Qty",
                        "Pakage No",
                        "Pakage Qty",
                        "Route&Qty",
                        "Uploaded By",
                        "Uploaded Date",
                    ]
                )


            for order_obj in order_list:

                order_row_list = (
                    order_obj.file_id,
                    order_obj.order_id,
                    order_obj.supplier_no,
                    order_obj.plant_no,
                    order_obj.part_number,
                    order_obj.due_date.strftime("%d/%m/%Y"),
                    order_obj.order_qty,
                    order_obj.package_no,
                    order_obj.package_qty,
                    order_obj.route_trip,
                    order_obj.updated_by,
                    order_obj.created_date.strftime("%d/%m/%Y")

                    )
                
                order_csv_list.append(order_row_list)

            name_csv_str = "PendingOrderCSV_" +datetime.now().strftime("%Y%m%d_%H%M%S")

            with open("media/" +  name_csv_str +'.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(order_csv_list)

            order_serializer = OrderSerializer(order_list, many=True)


            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "success"
            base_DTO_obj.massage = "get part"
            base_DTO_obj.data_list = order_serializer.data
            base_DTO_obj.csv_name =  name_csv_str + '.csv'

            order_list_Serializer_DTO = Order_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(order_list_Serializer_DTO.data,  safe=False)

        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "error"
            base_DTO_obj.massage = e
            base_DTO_obj.data_list =  None

            order_list_Serializer_DTO = Order_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(order_list_Serializer_DTO.data,safe=False)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def match_order(request):

    if request.method == 'POST':

        try :

            order_list = Order.objects.filter(updated_by= request.user.username, is_deleted = False )
            part_list = Part.objects.filter(is_active=True,status=2)
            route_list = RouterMaster.objects.filter(is_active=True)
            package_list = Package.objects.filter(is_active=True)

            for order_obj in [ order for order in order_list if order.is_part_completed == False or order.is_route_completed == False]  :
                
                check_part_list = [ part for part in part_list if 
                    part.part_number.strip().upper() == order_obj.part_number.strip().upper() 
                    ]
      
                if len(check_part_list) > 0 :

                    check_package_list = [ package for package in package_list if package.package_no.strip().upper() == check_part_list[0].package_no.strip().upper()]
                    if len(check_package_list) > 0:

                        Order.objects.filter(order_id = order_obj.order_id).update(
                            is_part_completed= True,
                            package_no = check_package_list[0].package_no,
                            package_qty = Decimal(math.ceil(order_obj.order_qty/check_package_list[0].snp)),
                            updated_by= request.user.username,
                            updated_date=datetime.utcnow()
                            )
                
                else:

                    Order.objects.filter(order_id = order_obj.order_id).update(
                        is_part_completed= False,package_no = '',
                        package_qty=0.00,
                        updated_by= request.user.username,
                        updated_date=datetime.utcnow()
                        )
                
                check_route_list = [ route for route in route_list if route.supplier_code.strip().upper() == order_obj.supplier_no.strip().upper() and 
                    route.plant_code.strip().upper() == order_obj.plant_no.strip().upper()
                    ]

                if len(check_route_list) > 0 :

                    Order.objects.filter(order_id = order_obj.order_id).update(
                        is_route_completed= True,
                        route_code=check_route_list[0].route_code,
                        route_trip=check_route_list[0].trip_no,
                        updated_by= request.user.username,
                        updated_date=datetime.utcnow())
                else:
                    
                    print("makky")
                    Order.objects.filter(order_id = order_obj.order_id).update(
                        is_route_completed= False,
                        route_code="",
                        route_trip="",
                        updated_by= request.user.username,
                        updated_date=datetime.utcnow())
        
            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "success"
            base_DTO_obj.massage = configMessage.configs.get("MATCH_ORDER_MASSAGE_SUCCESSFUL").data
            base_DTO_obj.data_list = None

            order_list_Serializer_DTO = Order_list_Serializer_DTO(base_DTO_obj)
            return JsonResponse(order_list_Serializer_DTO.data, safe=False)
        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "error"
            base_DTO_obj.massage = e
            base_DTO_obj.data_list = Order.objects.filter(is_deleted = False)

            order_list_Serializer_DTO = Order_list_Serializer_DTO(base_DTO_obj)
            return JsonResponse(order_list_Serializer_DTO.data, safe=False)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def search_upload_order_log_file(request):

    if request.method == 'POST':

        try:
            

            customer_selected = request.data['customer_selected']
            project_selected = request.data['project_selected']
            start_date_selected = request.data['start_date_selected']
            end_date_selected = request.data['end_date_selected']


            query = "select uploads_file.* from uploads_file "

            joint_str = "" 
            where_str = " where 1 = 1  and uploads_file.status = 2 "

            if customer_selected is not None:

                print(customer_selected)

                joint_str = joint_str + " INNER JOIN master_data_project "
                joint_str = joint_str + " ON master_data_project.project_code = uploads_file.project_id "
                joint_str = joint_str + " INNER JOIN master_data_customer "
                joint_str = joint_str + " ON master_data_customer.customer_code = master_data_project.customer_code "
                where_str = where_str + " and  uploads_file.customer_id = '%s' " % customer_selected
            
            if project_selected is not None:

                where_str = where_str + " and  uploads_file.project_id = '%s' " % project_selected
            
            if start_date_selected is not None and end_date_selected is not None:

                start_date_str = datetime.strptime(start_date_selected, "%d/%m/%Y").strftime("%Y/%m/%d")
                end_date_str = datetime.strptime(end_date_selected, "%d/%m/%Y").strftime("%Y/%m/%d")

                where_str = where_str + "and created_date between '%s' and '%s'" % (start_date_str,end_date_str)

            query = query + joint_str + where_str + "order by file_no desc"

            print(query)

            file_list = File.objects.raw(query)

            print(len(file_list))

            file_csv_list = []

            file_csv_list.insert(0, [
                        "Customer Code",
                        "Project",
                        "File No",
                        "Order Count",
                        "Status",
                        "Upload By",
                        "Upload Date"
                    ]
                )


            for file_obj in file_list:

                file_row_list = (
                    file_obj.customer_id,
                    file_obj.project_id,
                    file_obj.file_no,
                    file_obj.order_count,
                    'Confirm' if file_obj.status == 2 else 'Draft',
                    file_obj.created_by,
                    file_obj.created_date.strftime("%d/%m/%Y")

                    )
                
                file_csv_list.append(file_row_list)

            name_csv_str = "UloadOrderLogFileCSV_" +datetime.now().strftime("%Y%m%d_%H%M%S")
            with open("media/" +  name_csv_str +'.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(file_csv_list)


            file_serializer = FileSerializer(file_list, many=True)


            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "success"
            base_DTO_obj.massage = "get part"
            base_DTO_obj.data_list = file_serializer.data
            base_DTO_obj.csv_name =  name_csv_str + '.csv'

            file_list_Serializer_DTO = File_list_Serializer_DTO(base_DTO_obj)

            return JsonResponse(file_list_Serializer_DTO.data,  safe=False)

        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = e
            # base_DTO_obj.data = part_serializer_obj.data
            print(e);

            file_Serializer_DTO_reponse = File_Serializer_DTO(base_DTO_obj)

            return JsonResponse(file_Serializer_DTO_reponse.data,safe=False)

@api_view(['GET', 'POST', 'DELETE'])
def file_list(request):

    if request.method == 'GET':

        try : 

            file_list = File.objects.filter(status=2)
            print(file_list)
            file_serializer = FileSerializer(file_list, many=True)

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "success"
            base_DTO_obj.massage = "get file is success"
            base_DTO_obj.data_list = file_serializer.data

            file_list_Serializer_DTO_obj = File_list_Serializer_DTO(base_DTO_obj)


            return JsonResponse(file_list_Serializer_DTO_obj.data, safe=False)

        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = e
            base_DTO_obj.data = None

            file_Serializer_DTO_reponse = File_Serializer_DTO(base_DTO_obj)

            return JsonResponse(file_Serializer_DTO_reponse.data, safe=False)
    
@api_view(['GET', 'POST', 'DELETE'])
def order_list(request):

    if request.method == 'GET':

        try : 

            order_list = Order.objects.filter(is_part_completed=True,is_route_completed=True)
            order_serializer = OrderSerializer(order_list, many=True)

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "success"
            base_DTO_obj.massage = "get order is success"
            base_DTO_obj.data_list = order_serializer.data

            order_list_Serializer_DTO_obj = Order_list_Serializer_DTO(base_DTO_obj)


            return JsonResponse(order_list_Serializer_DTO_obj.data, safe=False)

        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = e
            base_DTO_obj.data = None

            order_Serializer_DTO_reponse = Order_Serializer_DTO(base_DTO_obj)

            return JsonResponse(order_Serializer_DTO_reponse.data, safe=False)


  



            # project_list =  Project.objects.filter(project_code = project_data['project_code'])

            # if len(project_list) > 0 :

            #     base_DTO_obj =  base_DTO()
            #     base_DTO_obj.serviceStatus = "Error"
            #     base_DTO_obj.massage = "Project Code is duplicate"
            #     base_DTO_obj.data = None

            #     project_Serializer_DTO_reponse = Project_Serializer_DTO(base_DTO_obj)

            #     return JsonResponse(project_list_serializer_DTO_reponse.data, safe=False) 

            

            if project_serializer_obj.is_valid():

                project_serializer_obj.save()
                # project_serializer_obj.save(updated_by=request.user.username,)

                base_DTO_obj =  base_DTO()
                base_DTO_obj.serviceStatus = "success"
                base_DTO_obj.massage = "project is saved"
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
            base_DTO_obj.massage = "someting is error"
            base_DTO_obj.data = None

            project_Serializer_DTO_reponse = Project_Serializer_DTO(base_DTO_obj)

            return JsonResponse(project_Serializer_DTO_reponse.data, safe=False)

@api_view(['POST'])
def search_order_transaction(request):

    if request.method == 'POST':

        try:

            customer_selected = request.data['customer_selected']
            project_selected = request.data['project_selected']
            start_date_selected = request.data['start_date_selected']
            end_date_selected = request.data['end_date_selected']
            file_selected = request.data['file_selected']
            order_selected = request.data['order_selected']
            file_selected = request.data['file_selected']
            order_selected = request.data['order_selected']
            supplier_selected = request.data['supplier_selected']
            plant_selected = request.data['plant_selected']

            query = "select * from order_order "

            joint_str = "" 
            where_str = " where 1 = 1    "

            if customer_selected is not None:

                print(customer_selected)

                joint_str = joint_str + " INNER JOIN master_data_project "
                joint_str = joint_str + " ON UPPER(master_data_project.project_code) = UPPER(order_order.project_code) "
                joint_str = joint_str + " INNER JOIN master_data_customer "
                joint_str = joint_str + " ON UPPER(master_data_customer.customer_code) = UPPER(master_data_project.customer_code) "
                where_str = where_str + " and  UPPER(master_data_customer.customer_code) = '%s' " % customer_selected.upper()
            
            if project_selected is not None:

                where_str = where_str + " and  UPPER(order_order.project_code) = '%s' " % project_selected.upper()

            if start_date_selected is not None and end_date_selected is not None:

                
                start_date_str = datetime.strptime(start_date_selected, "%d/%m/%Y").strftime("%Y/%m/%d")
                end_date_str = datetime.strptime(end_date_selected, "%d/%m/%Y").strftime("%Y/%m/%d")

                where_str = where_str + " and due_date between '%s' and '%s' " % (start_date_str,end_date_str)
            
            if file_selected is not None :

                where_str = where_str + " and  order_order.file_id = '%s' " % file_selected
            
            if order_selected is not None :

                where_str = where_str + " and  order_order.order_id = '%s' " % order_selected
            
            if supplier_selected is not None :

                where_str = where_str + " and  UPPER(order_order.supplier_no) = '%s' " % supplier_selected.upper()
            
            if plant_selected is not None :

                where_str = where_str + " and  UPPER(order_order.plant_no) = '%s' " % plant_selected.upper()
            
            query = query + joint_str + where_str + "order by order_order.order_id"


            order_csv_list = []

            order_csv_list.insert(0, [
                        "Action",
                        "File ID",
                        "Order ID",
                        "Supplier",
                        "Plant",
                        "Part No",
                        "Part Name",
                        "Due Date",
                        "Order Qty",
                        "Package No",
                        "Package Qty",
                        "Route&Trip",
                        "Uploaded By",
                        "Uploaded Date",
                    ]
                )
            

            order_list = Order.objects.raw(query)
            order_transaction_list_obj = []
            for order_obj in order_list :
            
                history_obj = json.loads(order_obj.history_updated) 

                order_transaction_obj = Order_transaction()
                order_transaction_obj.action = 'ADD'
                order_transaction_obj.file_id = order_obj.file_id
                order_transaction_obj.order_id = order_obj.order_id
                order_transaction_obj.supplier = order_obj.supplier_no
                order_transaction_obj.plant = order_obj.plant_no
                order_transaction_obj.part_no = order_obj.part_number
                part_list = Part.objects.filter(part_number= order_obj.part_number)
                if len(part_list) > 0 :
                    order_transaction_obj.part_name = part_list[0].part_name
                
                else:
                    order_transaction_obj.part_name = None

                order_transaction_obj.due_date = order_obj.due_date
                order_transaction_obj.order_qty = int(history_obj['add'])

                if order_obj.package_no == None or order_obj.package_no == "":

                    order_transaction_obj.package_no = None
                    order_transaction_obj.package_qty = None
                    order_transaction_obj.route_trip = None
                
                else : 

                    order_transaction_obj.package_no = order_obj.package_no
                    order_transaction_obj.package_qty = order_obj.package_qty
                    order_transaction_obj.route_trip = order_obj.route_trip

                order_transaction_obj.updated_by = order_obj.updated_by
                order_transaction_obj.updated_date = order_obj.updated_date

                order_transaction_list_obj.append(order_transaction_obj)

                order_row_list = (
                    'ADD',
                    order_obj.file_id,
                    order_obj.order_id,
                    order_obj.supplier_no,
                    order_obj.plant_no,
                    order_obj.part_number,
                    Part.objects.get(part_number= order_obj.part_number).part_name,
                    order_obj.due_date.strftime("%d/%m/%Y"),
                    int(history_obj['add']),
                    order_transaction_obj.package_no,
                    order_transaction_obj.package_qty,
                    order_transaction_obj.route_trip,
                    order_obj.updated_by,
                    order_obj.updated_date.strftime("%d/%m/%Y")
                    )


                order_csv_list.append(order_row_list) 

           

                for history_add_obj in history_obj['update'] :

                    order_transaction_obj = Order_transaction()
                    order_transaction_obj.action = 'UPDATE'
                    order_transaction_obj.file_id = order_obj.file_id
                    order_transaction_obj.order_id = order_obj.order_id
                    order_transaction_obj.supplier = order_obj.supplier_no
                    order_transaction_obj.plant = order_obj.plant_no
                    order_transaction_obj.part_no = order_obj.part_number
                    order_transaction_obj.part_name = Part.objects.get(part_number= order_obj.part_number).part_name
                    order_transaction_obj.due_date = order_obj.due_date
                    order_transaction_obj.order_qty = int(history_add_obj)

                    if order_obj.package_no == None or order_obj.package_no == "":

                        order_transaction_obj.package_no = None
                        order_transaction_obj.package_qty = None
                        order_transaction_obj.route_trip = None
                    
                    else : 

                        order_transaction_obj.package_no = order_obj.package_no
                        order_transaction_obj.package_qty = order_obj.package_qty
                        order_transaction_obj.route_trip = order_obj.route_trip

                    order_transaction_obj.updated_by = order_obj.updated_by
                    order_transaction_obj.updated_date = order_obj.updated_date

                    
                    order_transaction_list_obj.append(order_transaction_obj)

                    order_row_list = (
                        'UPDATE',
                        order_obj.file_id,
                        order_obj.order_id,
                        order_obj.supplier_no,
                        order_obj.plant_no,
                        order_obj.part_number,
                        Part.objects.get(part_number= order_obj.part_number).part_name,
                        order_obj.due_date.strftime("%d/%m/%Y"),
                        int(history_obj['add']),
                        order_transaction_obj.package_no,
                        order_transaction_obj.package_qty,
                        order_transaction_obj.route_trip,
                        order_obj.updated_by,
                        order_obj.updated_date.strftime("%d/%m/%Y")
                    )


                    order_csv_list.append(order_row_list) 

                for history_delete_obj in history_obj['delete'] :

                    order_transaction_obj = Order_transaction()
                    order_transaction_obj.action = 'DELETE'
                    order_transaction_obj.file_id = order_obj.file_id
                    order_transaction_obj.order_id = order_obj.order_id
                    order_transaction_obj.supplier = order_obj.supplier_no
                    order_transaction_obj.plant = order_obj.plant_no
                    order_transaction_obj.part_no = order_obj.part_number
                    order_transaction_obj.part_name = Part.objects.get(part_number= order_obj.part_number).part_name
                    order_transaction_obj.due_date = order_obj.due_date
                    order_transaction_obj.order_qty = int(history_delete_obj)
                    
                    if order_obj.package_no == None or order_obj.package_no == "":

                        order_transaction_obj.package_no = None
                        order_transaction_obj.package_qty = None
                        order_transaction_obj.route_trip = None
                
                    else : 

                        order_transaction_obj.package_no = order_obj.package_no
                        order_transaction_obj.package_qty = order_obj.package_qty
                        order_transaction_obj.route_trip = order_obj.route_trip
    
                    order_transaction_obj.updated_by = order_obj.updated_by
                    order_transaction_obj.updated_date = order_obj.updated_date

                    order_transaction_list_obj.append(order_transaction_obj)

                    order_row_list = (
                        'DELETE',
                        order_obj.file_id,
                        order_obj.order_id,
                        order_obj.supplier_no,
                        order_obj.plant_no,
                        order_obj.part_number,
                        Part.objects.get(part_number= order_obj.part_number).part_name,
                        order_obj.due_date.strftime("%d/%m/%Y") ,
                        int(history_obj['add']),
                        order_transaction_obj.package_no,
                        order_transaction_obj.package_qty,
                        order_transaction_obj.route_trip,
                        order_obj.updated_by,
                        order_obj.updated_date.strftime("%d/%m/%Y")
                    )


                    order_csv_list.append(order_row_list) 

                    

            name_csv_str = "OrderTransactionCSV_" +datetime.now().strftime("%Y%m%d_%H%M%S")

            with open("media/" +  name_csv_str +'.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(order_csv_list)
                     
            order_transaction_Serializer_obj = Order_transaction_Serializer(order_transaction_list_obj, many=True)

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "success"
            base_DTO_obj.massage = "project is saved"
            base_DTO_obj.csv_name = name_csv_str +'.csv'
            base_DTO_obj.data_list = order_transaction_Serializer_obj.data

            order_transaction_list__Serializer_DTO_obj = Order_transaction_list__Serializer_DTO(base_DTO_obj)
            return JsonResponse(order_transaction_list__Serializer_DTO_obj.data,  safe=False)
   

        except Exception as e:

            base_DTO_obj =  base_DTO()
            base_DTO_obj.serviceStatus = "Error"
            base_DTO_obj.massage = e
            base_DTO_obj.data = None

            file_Serializer_DTO_reponse = File_Serializer_DTO(base_DTO_obj)

            return JsonResponse(file_Serializer_DTO_reponse.data,safe=False)




   
            





        # file_deleted_obj = File.objects.filter(created_by= request.user.username, status = False)[0]
        # file_no_str = file_deleted_obj.file_no
        # file_file_str = file_deleted_obj.file

        # order_deleted_obj = Order.objects.filter(file_id = file_no_str)

        # file_deleted_obj.delete()
        # order_deleted_obj.delete()
        
        # os.remove("media/" + str(file_no_str) + ".csv")
        # os.remove("media/" + str(file_no_str) + "_database.csv")
        # os.remove("media/" + str(file_file_str))

        # file_list = File.objects.filter(created_by= request.user.username, status = False).values()
        # file_serializer = Plant_list_Serializer_DTO(file_list, many=True)

        # return JsonResponse(file_serializer.data, safe=False)




# @api_view(['GET', 'POST', 'DELETE'])
# def order_list(request):
#     # if request.method == 'GET':
#     #     tutorials = Tutorial.objects.all()
        
#     #     title = request.GET.get('title', None)
#     #     if title is not None:
#     #         tutorials = tutorials.filter(title__icontains=title)
        
#     #     tutorials_serializer = TutorialSerializer(tutorials, many=True)
#     #     return JsonResponse(tutorials_serializer.data, safe=False)
#     #     # 'safe=False' for objects serialization
#     if request.method == 'GET':
#         order_list = Order.objects.all()
        
#         # title = request.GET.get('title', None)
#         # if title is not None:
#         #     tutorials = tutorials.filter(title__icontains=title)
        
#         order_serializer = OrderSerializer(order_list, many=True)
#         return JsonResponse(order_serializer.data, safe=False)

 
#     elif request.method == 'POST':
#         order_data = JSONParser().parse(request)
#         order_serializer = OrderSerializer(data=order_data)
    
#         if order_serializer.is_valid():
#             # order_serializer.save()
#             return JsonResponse(order_serializer.data, status=status.HTTP_201_CREATED) 
#         return JsonResponse(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 