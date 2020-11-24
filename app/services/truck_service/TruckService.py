from order.models import Order
from django.db import connection
from order.serializers import OrderSerializer

cursor = connection.cursor()
class TruckService:


    def search_truck (self,truck_licese,province,truck_type,truck_fuel):
 
        cursor = connection.cursor()
        cursor.execute(" Begin;  SELECT * FROM search_truck(%s,%s,%s,%s);",['%'+truck_licese+'%',province,truck_type,truck_fuel]  )

        truck_list = cursor.fetchall()
        cursor.close();

        return truck_list

    