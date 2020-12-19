from order.models import Order
from django.db import connection
from order.serializers import OrderSerializer
from datetime import datetime
from truck_plan_management.serializers import PickUp_Serializer
from truck_plan_management.serializers import TruckPlan_Serializer,TruckPlan_Serializer_DTO,TruckPlan_Serializer_DTO
from app.helper.format.NumberFormat import NumberFormat


cursor = connection.cursor()

class TruckPlanManagementService:

    csv_list = []

    def search_generate_pickup(self,customer_code,project_code,due_date):

        cursor = connection.cursor()

        if due_date is not None :

            due_date = datetime.strptime(due_date, "%d/%m/%Y")

        cursor.execute(" Begin;  SELECT * FROM search_generate_pickup(%s,%s,%s);",[customer_code,project_code,due_date]  )

        pickup_list = cursor.fetchall()
        cursor.close();

        return pickup_list

      


    def search_pickUp_PUS(self,customer_code,project_code,supplier_code,due_date_from,due_date_to,PUS_ref):

        cursor = connection.cursor()

        if due_date_from is not None :

            due_date_from = datetime.strptime(due_date_from, "%d/%m/%Y")

        if due_date_to is not None :
            
            due_date_to = datetime.strptime(due_date_to, "%d/%m/%Y")
        
        if PUS_ref is not None :
            
            PUS_ref = "%"+PUS_ref+"%"
    
        cursor.execute(" Begin;  SELECT * FROM search_pickUp_PUS(%s,%s,%s,%s,%s,%s);",[customer_code,project_code,supplier_code,due_date_from,due_date_to,PUS_ref]  )

        pickup_list = cursor.fetchall()
        cursor.close();

        return pickup_list


    def search_generate_truck_plan(self,customer_code,project_code,due_date):


        if due_date is not None :

            due_date = datetime.strptime(due_date, "%d/%m/%Y")

        cursor = connection.cursor()

        cursor.execute(" Begin;  SELECT * FROM search_generate_truckplan(%s,%s,%s);",[customer_code,project_code,due_date]  )
        truckplan_list = cursor.fetchall()
        cursor.close();

        return truckplan_list


    def search_and_print_truck_plan(self,customer_code,project_code,due_date_from,due_date_to,truck_plan_ref):


        if due_date_from is not None :

            due_date_from = datetime.strptime(due_date_from, "%d/%m/%Y")

        if due_date_to is not None :
            
            due_date_to = datetime.strptime(due_date_to, "%d/%m/%Y")
        
        if truck_plan_ref is not None :
            
            truck_plan_ref = "%"+truck_plan_ref+"%"

        cursor = connection.cursor()

        cursor.execute(" Begin;  SELECT * FROM search_truckplan_pus(%s,%s,%s,%s,%s);",[customer_code,project_code,due_date_from,due_date_to,truck_plan_ref]  )
        truckplan_list = cursor.fetchall()
        cursor.close();

        return truckplan_list
        

    def pickup_report(self,pickup_no):

        cursor = connection.cursor()
        cursor.execute(" Begin;  CALL get_pickup_report(%s);",[pickup_no]  )
        cursor.execute(' FETCH ALL FROM "truck_plan_pickup_return";')
        truck_plan_pickup_return = cursor.fetchall()
        cursor.execute(' FETCH ALL FROM "order_order_return";')
        order_order_return = cursor.fetchall()
        cursor.close();

        return (truck_plan_pickup_return,order_order_return)
    

    def truck_report(self,truckplan_no):
 
        cursor = connection.cursor()
        cursor.execute(" Begin;  CALL get_truck_report(%s);",[truckplan_no]  )
        cursor.execute(' FETCH ALL FROM "truck_plan_return";')
        truck_plan_return = cursor.fetchall()
        cursor.execute(' FETCH ALL FROM "pickup_return";')
        pickup_return = cursor.fetchall()
        cursor.close();

        return (truck_plan_return,pickup_return)

        
