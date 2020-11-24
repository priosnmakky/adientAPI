from master_data.serializers import RouterInfo_Serializer
from app.helper.config.ConfigMessage import ConfigMessage
from datetime import datetime
from decimal import Decimal
import math
import re

class RouterInfoHelper:


    @staticmethod
    def covert_data_list_to_serializer_list(routerInfo_list) :

        routerInfo_return_list = []

        for routerInfo in routerInfo_list :

            routerInfo_Serializer = RouterInfo_Serializer()
            routerInfo_Serializer.id = routerInfo[0]
            routerInfo_Serializer.project_code = routerInfo[1]
            routerInfo_Serializer.route_code = routerInfo[2]
            routerInfo_Serializer.route_trip = routerInfo[3]
            routerInfo_Serializer.province = routerInfo[4]
            routerInfo_Serializer.truck_license = routerInfo[5]
            routerInfo_Serializer.driver_code = routerInfo[6]
            routerInfo_Serializer.driver_name = routerInfo[7]
            routerInfo_Serializer.updated_by = routerInfo[8]
            routerInfo_Serializer.updated_date = routerInfo[9]

            routerInfo_return_list.append(routerInfo_Serializer)
        
        return routerInfo_return_list


    @staticmethod
    def covert_data_list_to_CSV_list(routerInfo_list) :

        routerInfo_return_list = []

        for routerInfo_obj in routerInfo_list :

            routerInfo_return_list.append([
                routerInfo_obj[1],
                routerInfo_obj[2],
                routerInfo_obj[3],
                routerInfo_obj[4],
                routerInfo_obj[5],
                routerInfo_obj[7],
                routerInfo_obj[8],
                routerInfo_obj[9].strftime("%d/%m/%Y")

            ])
        
        return routerInfo_return_list
    
    

    