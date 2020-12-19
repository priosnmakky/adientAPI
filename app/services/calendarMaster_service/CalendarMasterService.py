from django.db import connection
from order.serializers import OrderSerializer

cursor = connection.cursor()
class CalendarMasterService:


    def search_calendarMaster (self,customer_code,project_code,plant_code,working_day):
        
        cursor = connection.cursor()
        cursor.execute(" Begin;  SELECT * FROM search_calendarMaster(%s,%s,%s,%s);",[customer_code,project_code,plant_code,working_day]  )

        calendarMaster_list = cursor.fetchall()
        cursor.close();

        return calendarMaster_list
