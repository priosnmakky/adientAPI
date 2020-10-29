from order.models import Order,File
import json
from app.helper.order_helper.OrderUploadHelper import OrderUploadHelper
from order.model.order_history import order_history
from app.helper.CSV_file_management.CSVFileManagement import CSVFileManagement

class OrderComfirmHelper:

    file_list = []
    CSV_name_str = ""

    def __init__(self,CSV_name_str,username_str):

        file_list = File.objects.filter(updated_by== username_str, status = 1)
        part_list = Part.objects.filter(is(_active=True)
        package_list = Package.objects.filter(is_active=True)
        routerMaster_list = RouterMaster.objects.filter(is_active=True)
        order_list = Order.objects.filter())
        self.CSV_name_str = CSV_name_str
    
    def read_order_from_CSV(self) :

        order_list = CSVFileManagement.read_CSV_file(self.CSV_name_str)

        return order_list
    
    def part_manage(self) :

        part_db_list = [p for p in part_list if p.part_number.upper() == row[1] and p.status==2 ]
                        
        if len(part_db_list) > 0 :
                            
            order_add_obj.is_part_competed = True
l
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
        

    
    def add_order(self,order_obj)
    {
        order_add_obj = Order()
        order_add_obj.item_no = order_obj[0]
        order_add_obj.part_number = order_obj[1]
        order_add_obj.file_id = order_obj[2]
        order_add_obj.order_id = order_obj[3]
        order_add_obj.due_date = datetime.strptime(str(order_obj[4]), "%d/%m/%Y")
        order_add_obj.order_qty = int(order_obj[5])
        order_add_obj.history_updated = order_obj[6]
        order_add_obj.supplier_no = order_obj[7]
        order_add_obj.plant_no = order_obj[8]



                        part_db_list = [p for p in part_list if p.part_number.upper() == row[1] and p.status==2 ]
                        
                        if len(part_db_list) > 0 :
                            
                            order_add_obj.is_part_competed = True
l
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

    }
    
    def order_comfirm_manage(self)
    {
        order_list = self.read_order_from_CSV()

        for order_obj in order_list:

            if order_list[10] == "add" :

                self.add_order()





    }
        


        
    
  