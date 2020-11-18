from order.models import Order
from django.db import connection
from order.serializers import OrderSerializer

cursor = connection.cursor()
class CustomerService:


    def search_customer (self,customer_code,project_code,station_code):
 
        cursor = connection.cursor()
        cursor.execute(" Begin;  SELECT * FROM search_customer(%s,%s,%s);",[customer_code,project_code,"%"+station_code+"%"]  )

        customer_list = cursor.fetchall()
        cursor.close();

        return customer_list
