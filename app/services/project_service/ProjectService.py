from order.models import Order
from django.db import connection
from order.serializers import OrderSerializer

cursor = connection.cursor()
class ProjectService:


    def search_project (self,customer_code):
 
        cursor = connection.cursor()
        cursor.execute(" Begin;  SELECT * FROM search_project(%s);",[customer_code]  )

        project_list = cursor.fetchall()
        cursor.close();

        return project_list
