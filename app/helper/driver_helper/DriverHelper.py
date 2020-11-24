from datetime import datetime
from decimal import Decimal
from master_data.serializers import Driver_Serializer
import math

class DriverHelper:

    
    @staticmethod
    def covert_data_list_to_serializer_list(driver_list) :

        driver_return_list = []

        for driver_obj in driver_list :

            driver_Serializer = Driver_Serializer()
            driver_Serializer.driver_code = driver_obj[0]
            driver_Serializer.name = driver_obj[1]
            driver_Serializer.tel = driver_obj[2]
            driver_Serializer.remark = driver_obj[3]
            driver_Serializer.updated_by = driver_obj[4]
            driver_Serializer.updated_date = driver_obj[5]


            driver_return_list.append(driver_Serializer)
        
        return driver_return_list
    
    @staticmethod
    def covert_data_list_to_CSV_list(driver_list) :

        driver_return_list = []

        for driver_obj in driver_list :

            driver_return_list.append([
                driver_obj[0],
                driver_obj[1],
                driver_obj[2],
                driver_obj[3],
                driver_obj[4],
                driver_obj[5].strftime("%d/%m/%Y"),

            ])
        
        return driver_return_list

    