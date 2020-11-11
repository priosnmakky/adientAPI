from master_data.models import Part,RouterMaster,Package
from order.models import Order
from order.serializers import OrderSerializer
from datetime import datetime
from decimal import Decimal
import math

class OrderMissMatchHelper:

    order_list = []
    part_list = []
    route_list = []
    package_list = []
    username = ""
    
    def __init__(self,username):

        self.order_list = Order.objects.filter(updated_by= username, is_deleted = False )
        self.part_list = Part.objects.filter(is_active=True,status=2)
        self.route_list = RouterMaster.objects.filter(is_active=True)
        self.package_list = Package.objects.filter(is_active=True)
        self.username = username

    def part_management(self,order_obj):

        check_part_list = [ part for part in self.part_list if 
                    part.part_number.strip().upper() == order_obj.part_number.strip().upper() 
                    ]
        
        if len(check_part_list) > 0 :

            check_package_list = [ package for package in self.package_list if package.package_no.strip().upper() == check_part_list[0].package_no.strip().upper()]
            
            if len(check_package_list) > 0:
                Order.objects.filter(order_no = order_obj.order_no).update(
                    is_part_completed= True,
                    package_no = check_package_list[0].package_no,
                    package_qty = Decimal(math.ceil(order_obj.order_qty/check_package_list[0].snp)),
                    updated_by= self.username,
                    updated_date=datetime.utcnow()
                )

            else:

                    Order.objects.filter(order_no = order_obj.order_no).update(
                        is_part_completed= False,package_no = '',
                        package_qty=0.00,
                        updated_by= self.username,
                        updated_date=datetime.utcnow()
                        )

    def route_management(self,order_obj):

        check_route_list = [ route for route in self.route_list if route.supplier_code.strip().upper() == order_obj.supplier_code.strip().upper() and 
                    route.plant_code.strip().upper() == order_obj.plant_code.strip().upper()
                    ]          
        
        if len(check_route_list) > 0 :

            Order.objects.filter(order_no = order_obj.order_no).update(
                is_route_completed= True,
                route_code=check_route_list[0].route_code,
                route_trip=check_route_list[0].route_trip,
                updated_by= self.username,
                updated_date=datetime.utcnow())
        else:
                    
            Order.objects.filter(order_no = order_obj.order_no).update(
                is_route_completed= False,
                route_code="",
                route_trip="",
                updated_by= self.username,
                updated_date=datetime.utcnow())


    def miss_match_management(self):

        order_list = [ order for order in self.order_list if order.is_part_completed == False or order.is_route_completed == False] 

        for order_obj in order_list :

            self.part_management(order_obj)

            self.route_management(order_obj)
        

        return order_list
    
    @staticmethod
    def covert_data_list_to_serializer_list(order_list) :

        order_return_list = []

        for order_obj in order_list :

            orderSerializer = OrderSerializer()
            orderSerializer.is_part_completed = order_obj[0]
            orderSerializer.is_route_completed = order_obj[1]
            orderSerializer.file_no = order_obj[2]
            orderSerializer.order_no = order_obj[3]
            orderSerializer.supplier_code = order_obj[4]
            orderSerializer.plant_code = order_obj[5]
            orderSerializer.part_number  = order_obj[6]
            orderSerializer.part_name  = order_obj[7]
            orderSerializer.due_date  = order_obj[8]
            orderSerializer.order_qty  = order_obj[9]
            orderSerializer.package_no  = order_obj[10]
            orderSerializer.package_qty  = order_obj[11]
            orderSerializer.route_code  = order_obj[12]
            orderSerializer.route_trip  = order_obj[13]
            orderSerializer.updated_by  = order_obj[14]
            orderSerializer.updated_date  = order_obj[15]

            order_return_list.append(orderSerializer)
        
        return order_return_list
    
    @staticmethod
    def covert_data_list_to_CSV_list(order_list) :

        order_return_list = []

        for order_obj in order_list :

            order_return_list.append([
               order_obj[2],
               order_obj[3],
               order_obj[4],
               order_obj[5],
               order_obj[7],
               order_obj[8].strftime("%d/%m/%Y"),
               order_obj[9],
               order_obj[10],
               "" if order_obj[10] == None or order_obj[10] == ""  else order_obj[11],
               "" if order_obj[12] == None or order_obj[12] == ""  else order_obj[12] + "-" +order_obj[13],
               order_obj[14],
               order_obj[15].strftime("%d/%m/%Y")
            ])
        
        return order_return_list

   