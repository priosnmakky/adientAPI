from order.models import Order
from django.db import connection
from order.serializers import OrderSerializer

cursor = connection.cursor()
class PartService:

    def search_part (self,customer_code,project_code,supplier_code,status,part_number):
 
        cursor = connection.cursor()
        cursor.execute(" Begin;  SELECT * FROM search_part(%s,%s,%s,%s,%s);",[customer_code,project_code,supplier_code,status,"%"+part_number+"%"]  )

        part_list = cursor.fetchall()
        cursor.close();

        return part_list
