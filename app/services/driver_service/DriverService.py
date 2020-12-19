from order.models import Order
from django.db import connection
from order.serializers import OrderSerializer

cursor = connection.cursor()
class DriverService:

    def search_driver(self,driver_code,driver_name):
 
        cursor = connection.cursor()
        cursor.execute(" Begin;  SELECT * FROM search_driver(%s,%s);",["%"+driver_code+"%","%"+driver_name+"%"]  )

        driver_list = cursor.fetchall()
        cursor.close();

        return driver_list
