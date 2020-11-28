from order.serializers import OrderSerializer
from datetime import datetime
from decimal import Decimal
import math

class PickupGenHelper:

    
    @staticmethod
    def covert_data_list_to_serializer_list(pickup_list) :

        pickup_return_list = []

        for pickup_obj in pickup_list :

            order_serializer_obj = OrderSerializer()

            order_serializer_obj.pickup_no = pickup_obj[0]
            order_serializer_obj.supplier_code = pickup_obj[1]
            order_serializer_obj.plant_code = pickup_obj[2]
            order_serializer_obj.route_code = pickup_obj[3]
            order_serializer_obj.route_trip = pickup_obj[4]
            order_serializer_obj.due_date = pickup_obj[5]
            order_serializer_obj.order_count = pickup_obj[6]
        

            pickup_return_list.append(order_serializer_obj)
        
        return pickup_return_list
    
    @staticmethod
    def covert_data_list_to_CSV_list(project_list) :

        project_return_list = []

        for project_obj in project_list :

            project_return_list.append([
                project_obj[0],
                project_obj[1],
                project_obj[2],
                project_obj[3],
                project_obj[4].strftime("%d/%m/%Y")

            ])
        
        return project_return_list

    