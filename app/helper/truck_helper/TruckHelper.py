from master_data.serializers import Truck_Serializer
from datetime import datetime
from decimal import Decimal
import math

class TruckHelper:

    
    @staticmethod
    def covert_data_list_to_serializer_list(truck_list) :

        truck_return_list = []

        for truck_obj in truck_list :

            truck_serializer = Truck_Serializer()
            truck_serializer.truck_license = truck_obj[0]
            truck_serializer.province = truck_obj[1]
            truck_serializer.truck_type = truck_obj[2]
            truck_serializer.fuel_type = truck_obj[3]
            truck_serializer.max_speed = truck_obj[4]
            truck_serializer.max_volume = truck_obj[5]
            truck_serializer.max_weight = truck_obj[6]
            truck_serializer.remark = truck_obj[7]
            truck_serializer.updated_by = truck_obj[8]
            truck_serializer.updated_date = truck_obj[9]

            truck_return_list.append(truck_serializer)
        
        return truck_return_list
    
    @staticmethod
    def covert_data_list_to_CSV_list(truck_list) :

        truck_return_list = []

        for truck_obj in truck_list :

            truck_return_list.append([
                truck_obj[0],
                truck_obj[1],
                truck_obj[2],
                truck_obj[3],
                truck_obj[4],
                truck_obj[5],
                truck_obj[6],
                truck_obj[7],
                truck_obj[8],
                truck_obj[9].strftime("%d/%m/%Y"),

            ])
        
        return truck_return_list

    