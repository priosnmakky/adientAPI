from order.models import Order
from django.db import connection
from order.serializers import OrderSerializer

cursor = connection.cursor()
class RouterInfoService:


    def search_RouterInfo(self,customer_code,project_code,route_code,route_trip):
 
        cursor = connection.cursor()
        cursor.execute(" Begin;  SELECT * FROM search_routeInfo(%s,%s,%s,%s);",[customer_code,project_code,route_code,route_trip]  )

        routerInfo_list = cursor.fetchall()
        cursor.close();

        return routerInfo_list
    
 