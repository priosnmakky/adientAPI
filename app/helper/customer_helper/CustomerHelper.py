from datetime import datetime
from decimal import Decimal
from master_data.serializers import Customer_Serializer
import math

class CustomerHelper:

    
    @staticmethod
    def covert_data_list_to_serializer_list(customer_list) :

        customer_return_list = []

        for customer_obj in customer_list :

            customer_Serializer = Customer_Serializer()
            customer_Serializer.customer_code = customer_obj[0]
            customer_Serializer.project_code = customer_obj[1]
            customer_Serializer.station_code = customer_obj[2]
            customer_Serializer.description = customer_obj[3]
            customer_Serializer.station_type = customer_obj[4]
            customer_Serializer.zone = customer_obj[5]
            customer_Serializer.province = customer_obj[6]
            customer_Serializer.address = customer_obj[7]
            customer_Serializer.remark = customer_obj[8]
            customer_Serializer.updated_by = customer_obj[9]
            customer_Serializer.updated_date = customer_obj[10]

            customer_return_list.append(customer_Serializer)
        
        return customer_return_list
    
    @staticmethod
    def covert_data_list_to_CSV_list(customer_list) :

        customer_return_list = []

        for customer_obj in customer_list :

            customer_return_list.append([
                customer_obj[0],
                customer_obj[1],
                customer_obj[2],
                customer_obj[3],
                customer_obj[4],
                customer_obj[5],
                customer_obj[6],
                customer_obj[7],
                customer_obj[8],
                customer_obj[9],
                customer_obj[10].strftime("%d/%m/%Y"),

            ])
        
        return customer_return_list

    