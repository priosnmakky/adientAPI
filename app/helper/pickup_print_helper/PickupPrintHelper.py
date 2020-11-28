from truck_plan_management.serializers import PickUp_Serializer
from datetime import datetime
from decimal import Decimal
import math
from app.helper.format.NumberFormat import NumberFormat

class PickupPrintHelper:

    
    @staticmethod
    def covert_data_list_to_serializer_list(pickup_list) :

        pickup_return_list = []
        
        for pickUp_obj in pickup_list :

            pickUp_serializer_obj = PickUp_Serializer()

            pickUp_serializer_obj.pickup_no = pickUp_obj[0]
            pickUp_serializer_obj.status = pickUp_obj[1]
            pickUp_serializer_obj.supplier_code = pickUp_obj[2]
            pickUp_serializer_obj.plant_code = pickUp_obj[3]
            pickUp_serializer_obj.order_count = pickUp_obj[4]
            pickUp_serializer_obj.due_date = datetime.strptime(pickUp_obj[5].strftime("%Y-%m-%d"), "%Y-%m-%d")
            pickUp_serializer_obj.release_time = pickUp_obj[6]
            pickUp_serializer_obj.delivery_time = pickUp_obj[7]
            pickUp_serializer_obj.route_code = pickUp_obj[8]
            pickUp_serializer_obj.route_trip = pickUp_obj[9]
            pickUp_serializer_obj.truck_license = pickUp_obj[10]
            pickUp_serializer_obj.name = pickUp_obj[11]


            pickup_return_list.append(pickUp_serializer_obj)
        
        return pickup_return_list
    
    @staticmethod
    def covert_data_list_to_CSV_list(pickUp_list) :

        pickUp_return_list = []

        for pickUp_obj in pickUp_list :

            pickUp_return_list.append([
                pickUp_obj[0],
                "Complete" if pickUp_obj[1] == 2 else "Waiting",
                pickUp_obj[2],
                pickUp_obj[3],
                pickUp_obj[4],
                datetime.strptime(pickUp_obj[5].strftime("%Y-%m-%d"), "%Y-%m-%d").date(),
                NumberFormat.formal_decimal(pickUp_obj[6]),
                NumberFormat.formal_decimal(pickUp_obj[7]),
                pickUp_obj[8],
                pickUp_obj[9],
                pickUp_obj[10],
                pickUp_obj[11]

            ])
        
        return pickUp_return_list

    