from truck_plan_management.serializers import TruckPlan_Serializer
from datetime import datetime
from decimal import Decimal
import math
from app.helper.format.NumberFormat import NumberFormat

class TruckGenHelper:

    
    @staticmethod
    def covert_data_list_to_serializer_list(truckplan_list) :

        truckplan_return_list = []
        
        for truckplan_obj in truckplan_list :

            truckplan_serializer_obj = TruckPlan_Serializer()

            truckplan_serializer_obj.truckplan_no = truckplan_obj[0]
            truckplan_serializer_obj.pickUp_count = truckplan_obj[1]
            truckplan_serializer_obj.due_date = truckplan_obj[2]
            truckplan_serializer_obj.route_code = truckplan_obj[3]
            truckplan_serializer_obj.route_trip = truckplan_obj[4]

            truckplan_return_list.append(truckplan_serializer_obj)
        
        return truckplan_return_list
    
    @staticmethod
    def covert_data_list_to_CSV_list(truckplan_list) :

        truckplan_return_list = []

        for truckplan_obj in truckplan_list :

            truckplan_return_list.append([
                truckplan_obj[0],
                truckplan_obj[1],
                datetime.strptime(truckplan_obj[2].strftime("%Y-%m-%d"), "%Y-%m-%d"),
                truckplan_obj[3],
                truckplan_obj[4]

            ])

     
        
        return truckplan_return_list

    