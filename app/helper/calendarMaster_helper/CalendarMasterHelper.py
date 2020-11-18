from datetime import datetime
from decimal import Decimal
from master_data.serializers import CalendarMaster_Serializer
import math

class CalendarMasterHelper:

    
    @staticmethod
    def covert_data_list_to_serializer_list(calendarMaster_list) :

        calendarMaster_return_list = []

        for calendarMaster_obj in calendarMaster_list :

            calendarMaster_Serializer = CalendarMaster_Serializer()
            calendarMaster_Serializer.plant_code = calendarMaster_obj[0]
            calendarMaster_Serializer.day = calendarMaster_obj[1]
            calendarMaster_Serializer.date = calendarMaster_obj[2]
            calendarMaster_Serializer.is_working = calendarMaster_obj[3]
            calendarMaster_Serializer.remark = calendarMaster_obj[4]
            calendarMaster_Serializer.updated_by = calendarMaster_obj[5]
            calendarMaster_Serializer.updated_date = calendarMaster_obj[6]

            calendarMaster_return_list.append(calendarMaster_Serializer)
        
        return calendarMaster_return_list

    @staticmethod
    def covert_to_date_str(date_int):

        if date_int == 1 :

            return "Sunday"
        
        if date_int == 2 :

            return "Monday"
        
        if date_int == 3 :

            return "Tuesday"
        
        if date_int == 4 :

            return "Wednesday"
        
        if date_int == 5 :

            return "Thursday"
        
        if date_int == 6 :

            return "Friday"

        if date_int == 7 :

            return "Saturday"
    
    @staticmethod
    def covert_data_list_to_CSV_list(calendarMaster_list) :

        calendarMaster_return_list = []

        for calendarMaster_obj in calendarMaster_list :

            print(calendarMaster_obj[1])
            calendarMaster_return_list.append([
                calendarMaster_obj[0],
                CalendarMasterHelper.covert_to_date_str(int(calendarMaster_obj[1])),
                calendarMaster_obj[2],
                "Yes" if calendarMaster_obj[3]  else "No",
                calendarMaster_obj[4],
                calendarMaster_obj[5],
                calendarMaster_obj[6].strftime("%d/%m/%Y")

            ])
        
        return calendarMaster_return_list

    