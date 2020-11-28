from order.models import Order,File
from master_data.models import Part,Package,RouterMaster
# import json
from app.helper.order_helper.OrderUploadHelper import OrderUploadHelper
# from order.model.order_history import order_history
from app.helper.CSV_file_management.CSVFileManagement import CSVFileManagement
import csv
from datetime import datetime
import math

class OrderComfirmHelper:

    file_list = []
    CSV_name_str = ""
    project_code = ""
    updated_by = ""


    def __init__(self,username_str):

        self.file_list = File.objects.filter(updated_by= username_str, status = 1)
        self.part_list = Part.objects.filter(is_active=True)
        self.package_list = Package.objects.filter(is_active=True)
        self.routerMaster_list = RouterMaster.objects.filter(is_active=True)
        self.order_list = Order.objects.filter()
        self.project_code = self.file_list[0].project_code
        self.CSV_name_str = "media/" + str(self.file_list[0].file_no) + "DatabaseCSV.csv" 
        self.updated_by = username_str
    
    def read_order_from_CSV(self) :
       
        order_csv_list = CSVFileManagement.read_CSV_file(self.CSV_name_str,';','|')

        return order_csv_list
    
    def add_part(self,part_number,supplier_code,part_name,package_no) :
    
        part = Part()
        part.part_number  = part_number
        part.project_code = self.project_code
        part.supplier_code = supplier_code
        part.part_name = part_name
        part.package_no = package_no
        part.updated_by = self.updated_by
        part.is_active = True
        part.status = 1   
        part.save()

        return part

    
    def add_order(self,order_obj) :

        order_add_obj = Order()
        order_add_obj.item_no = order_obj[0]
        order_add_obj.part_number = order_obj[1]
        order_add_obj.file_no = order_obj[2]
        order_add_obj.order_no = order_obj[3]
        order_add_obj.due_date = datetime.strptime(str(order_obj[4]), "%d/%m/%Y %H:%M")
        order_add_obj.order_qty = int(order_obj[5])
        order_add_obj.history_updated = order_obj[6]
        order_add_obj.supplier_code = order_obj[7]
        order_add_obj.plant_code = order_obj[8]
        order_add_obj.project_code = self.project_code
        order_add_obj.updated_by = self.updated_by
        order_add_obj.updated_date = datetime.utcnow()

        part_db_list = [p for p in self.part_list if p.part_number.upper() == order_obj[1] and p.status==2 ]
                        
        if len(part_db_list) > 0 :
                            
            order_add_obj.is_part_completed = True

            package_db_list = [p for p in self.package_list if p.package_no.upper() == part_db_list[0].package_no.upper() ]

            if len(package_db_list) > 0 :
                                
                order_add_obj.package_no = package_db_list[0].package_no
                order_add_obj.package_qty = math.ceil(int(order_obj[5])/package_db_list[0].snp)
                            
        else :
                            
            check_part_list  = Part.objects.filter(part_number=order_obj[1])
                            
            order_add_obj.is_part_completed = False

            if len(check_part_list) == 0  :
 
                self.add_part(order_obj[1],order_obj[7],order_obj[9],None)
                    
        routerMaster_db_list = [r for r in self.routerMaster_list if r.supplier_code.upper() == order_obj[7].upper() and r.plant_code.upper() == order_obj[8].upper() ]

        if len(routerMaster_db_list) > 0 :
                    
            order_add_obj.is_route_completed = True
            order_add_obj.route_trip = routerMaster_db_list[0].route_trip
            order_add_obj.route_code = routerMaster_db_list[0].route_code

        else :

            order_add_obj.is_route_completed = False
            
        
        
        order_add_obj.save()

        return order_add_obj


    def update_order(self,order_obj) :

        order_update_obj= Order.objects.filter(order_no__iexact=order_obj[3])
        order_update_obj.update(
            order_qty=int(order_obj[5]),
            history_updated=order_obj[6],
            updated_date=datetime.utcnow(),
            updated_by=self.updated_by,
            is_deleted=False)
        
        return order_update_obj

    
    def delete_order(self,order_obj) :

        order_update_obj = Order.objects.filter(order_no__iexact=order_obj[3])
        order_update_obj.update(
            history_updated=order_obj[6],
            updated_date=datetime.utcnow(),
            updated_by=self.updated_by,
            is_deleted=True)
        
        return order_update_obj

    
    def order_comfirm_manage(self) :

        order_return_list = []
        with open(self.CSV_name_str, newline='') as csvfile:

            order_csv_list = csv.reader(csvfile, delimiter=';', quotechar='|')

            for order_obj in order_csv_list:
                
                if order_obj[10] == "add" :

                    order_return_obj = self.add_order(order_obj)
                    order_return_list.append(order_return_obj)

                
                if order_obj[10] == "update" :

                    order_return_obj = self.update_order(order_obj)
                    order_return_list.append(order_return_obj)
                
                if order_obj[10] == "delete" :

                    order_return_obj = self.delete_order(order_obj)
                    order_return_list.append(order_return_obj)
                    
            self.file_list.update(status = 2)

        return order_return_list
    
   

        
    
  