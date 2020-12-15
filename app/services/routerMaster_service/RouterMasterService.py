from order.models import Order
from django.db import connection
from order.serializers import OrderSerializer

cursor = connection.cursor()
class RouterMasterService:


    def search_routerMaster (self,customer_code,project_code,supplier_code,plant_code,route_code,route_trip):
 
        cursor = connection.cursor()
        cursor.execute(" Begin;  SELECT * FROM search_routeMaster(%s,%s,%s,%s,%s,%s);",[customer_code,project_code,supplier_code,plant_code,route_code,route_trip]  )

        routerMaster_list = cursor.fetchall()
        cursor.close();

        return routerMaster_list
    
    def update_routerMaster (self,reuterMaster_list):
 
        cursor = connection.cursor()

        
        sql = "   SELECT * FROM updated_route_master(%s::route_master[]) "
        sql = sql +"as dept(project_code character varying,route_code character varying,route_trip character varying,supplier_code character varying,"
        sql = sql +" plant_code character varying,pickup_before integer,release_time  character varying , pickup_time  character varying , depart_time character varying,"
        sql = sql +" delivery_time character varying, complete_time character varying);"

        cursor.execute( sql,[reuterMaster_list] )

        routerMaster_list = cursor.fetchall()

        cursor.close();

        return routerMaster_list

   