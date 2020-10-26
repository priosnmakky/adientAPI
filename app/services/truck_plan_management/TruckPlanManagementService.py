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

    def search_order_for_generate_pickup(self,customer_code_selected_str,project_code_selected_str,due_date_selected_str):


        query_first = "SELECT truck_plan_management_pickup.pickup_no,truck_plan_management_pickup.supplier_code,truck_plan_management_pickup.plant_code,truck_plan_management_pickup.route_code,truck_plan_management_pickup.route_trip,truck_plan_management_pickup.due_date,COUNT(order_order.order_id)  FROM truck_plan_management_pickup  "

        joint_str_first = " LEFT JOIN order_order ON order_order.pickup_no = truck_plan_management_pickup.pickup_no and order_order.is_deleted = false and order_order.is_part_completed = true and order_order.is_route_completed = true   "
        where_str_first = " where 1 = 1  "

        query_second = "SELECT order_order.pickup_no,order_order.supplier_no,order_order.plant_no,order_order.route_code,order_order.route_trip,order_order.due_date,COUNT(order_order.order_id) FROM order_order "

        joint_str_second  = ""
        where_str_second  = " where order_order.is_deleted = false and order_order.is_part_completed = true and order_order.is_route_completed = true "

        if customer_code_selected_str is not None and customer_code_selected_str != "":
            
            joint_str_first = joint_str_first + " INNER JOIN master_data_routermaster " 
            joint_str_first = joint_str_first + " ON UPPER(master_data_routermaster.route_code) = UPPER(truck_plan_management_pickup.route_code) "
            joint_str_first = joint_str_first + " and UPPER(master_data_routermaster.trip_no) = UPPER(truck_plan_management_pickup.route_trip) "
            
            joint_str_first = joint_str_first + " INNER JOIN master_data_project  "
            joint_str_first = joint_str_first + " ON UPPER(master_data_project.project_code) = UPPER(master_data_routermaster.project_code) "
            
            joint_str_first = joint_str_first + " INNER JOIN master_data_customer "
            joint_str_first = joint_str_first + " ON UPPER(master_data_customer.customer_code) = UPPER(master_data_project.customer_code) "

            where_str_first = where_str_first + " and   UPPER(master_data_customer.customer_code) = '%s' " % customer_code_selected_str.upper()

            joint_str_second = joint_str_second + " INNER JOIN master_data_project "
            joint_str_second = joint_str_second + " ON UPPER(master_data_project.project_code) = UPPER(order_order.project_code) "

            joint_str_second = joint_str_second + " INNER JOIN master_data_customer "
            joint_str_second = joint_str_second + " ON UPPER(master_data_customer.customer_code) = UPPER(master_data_project.customer_code) "
                    
            where_str_second = where_str_second + " and   UPPER(master_data_customer.customer_code) = '%s' " % customer_code_selected_str.upper()

        if project_code_selected_str is not None and project_code_selected_str != "":

            where_str_first = where_str_first + " and   UPPER(order_order.project_code) = '%s' " % project_code_selected_str.upper()

            where_str_second = where_str_second + " and   UPPER(order_order.project_code) = '%s' " % project_code_selected_str.upper()

        if due_date_selected_str is not None :

            due_date_selected_str = datetime.strptime(due_date_selected_str, "%d/%m/%Y").strftime("%Y/%m/%d")
            where_str_first = where_str_first + "and truck_plan_management_pickup.due_date = '%s' " % due_date_selected_str

            where_str_second = where_str_second + "and order_order.due_date = '%s' " % due_date_selected_str

        query_first = query_first + joint_str_first + where_str_first + " GROUP BY truck_plan_management_pickup.pickup_no,truck_plan_management_pickup.supplier_code,truck_plan_management_pickup.plant_code, truck_plan_management_pickup.route_code,truck_plan_management_pickup.route_trip,truck_plan_management_pickup.due_date  "

        query_second = query_second + joint_str_second + where_str_second + " GROUP BY order_order.pickup_no,order_order.supplier_no,order_order.plant_no, order_order.route_code,order_order.route_trip,order_order.due_date   "
      
        cursor.execute(query_first + " UNION " + query_second + " Order by pickup_no")
        result_order_list = cursor.fetchall()
        

        return_order_list = []

        for order_obj in result_order_list :

            orderSerializer_obj = OrderSerializer()
            orderSerializer_obj.pickup_no = order_obj[0]
            orderSerializer_obj.supplier_no = order_obj[1]
            orderSerializer_obj.plant_no = order_obj[2]
            orderSerializer_obj.route_code = order_obj[3]
            orderSerializer_obj.route_trip = order_obj[4]
            orderSerializer_obj.due_date = datetime.strptime(order_obj[5].strftime("%Y-%m-%d"), "%Y-%m-%d")
            orderSerializer_obj.order_count = order_obj[6]
            
            return_order_list.append(orderSerializer_obj)
        
        return return_order_list


    def search_pickUp_PUS(self,customer_code_selected_str,project_code_selected_str,supplier_code_selected_str,due_date_from_selected_str,due_date_to_selected_str,PUS_ref_selected_str):


        query = "SELECT truck_plan_management_pickup.pickup_no,truck_plan_management_pickup.supplier_code,truck_plan_management_pickup.plant_code,truck_plan_management_pickup.due_date,master_data_routermaster.release_time,master_data_routermaster.delivery_time,master_data_routermaster.route_code,master_data_routermaster.trip_no,master_data_routerinfo.truck_license,master_data_driver.name,COUNT(order_order.*),truck_plan_management_pickup.status"
        query = query + " FROM truck_plan_management_pickup "
        joint_str = " left join order_order ON order_order.pickup_no = truck_plan_management_pickup.pickup_no left join master_data_routermaster "
        joint_str = joint_str + " ON master_data_routermaster.route_code = truck_plan_management_pickup.route_code and master_data_routermaster.trip_no = truck_plan_management_pickup.route_trip "
        joint_str = joint_str + " left join master_data_routerinfo ON master_data_routerinfo.route_code = master_data_routermaster.route_code "
        joint_str = joint_str + " and master_data_routerinfo.trip_no = master_data_routermaster.trip_no "
        joint_str = joint_str + " left join master_data_driver ON master_data_driver.driver_code = master_data_routerinfo.driver_code "

        group_by = "GROUP BY truck_plan_management_pickup.pickup_no,"
        group_by = group_by + "truck_plan_management_pickup.supplier_code,"
        group_by = group_by + "truck_plan_management_pickup.plant_code,"
        group_by = group_by + "truck_plan_management_pickup.due_date,"
        group_by = group_by + "master_data_routermaster.release_time,"
        group_by = group_by + "master_data_routermaster.delivery_time,"
        group_by = group_by + "master_data_routermaster.route_code,"
        group_by = group_by + "master_data_routermaster.trip_no,"
        group_by = group_by + "master_data_routerinfo.truck_license,"
        group_by = group_by + "master_data_driver.name,"
        group_by = group_by + "truck_plan_management_pickup.status"
        where_str = " where 1 = 1  "

        if customer_code_selected_str is not None and customer_code_selected_str != "":

            joint_str = joint_str + " left join master_data_project "
            joint_str = joint_str + " ON  UPPER(master_data_project.project_code) = UPPER(master_data_routermaster.project_code) "
            joint_str = joint_str + " left join master_data_customer "
            joint_str = joint_str + " ON UPPER(master_data_customer.customer_code) =  UPPER(master_data_project.customer_code) "

            where_str = where_str + " and UPPER(master_data_customer.customer_code) = '%s' " % customer_code_selected_str.upper()
        
        if project_code_selected_str is not None and project_code_selected_str != "":

            where_str = where_str + " and   UPPER(master_data_project.project_code) = '%s' " % project_code_selected_str.upper()

        if due_date_from_selected_str is not None and due_date_to_selected_str is None:

            due_date_from_selected_str = datetime.strptime(due_date_from_selected_str, "%d/%m/%Y").strftime("%Y/%m/%d")
            where_str = where_str + "and truck_plan_management_pickup.due_date  >= '%s' " % due_date_from_selected_str
        
        if due_date_from_selected_str is  None and due_date_to_selected_str is not None:

            due_date_to_selected_str = datetime.strptime(due_date_to_selected_str, "%d/%m/%Y").strftime("%Y/%m/%d")
            where_str = where_str + "and truck_plan_management_pickup.due_date <= '%s' " % due_date_to_selected_str

        if due_date_from_selected_str is not None and due_date_to_selected_str is not None:

            due_date_from_selected_str = datetime.strptime(due_date_from_selected_str, "%d/%m/%Y").strftime("%Y/%m/%d")
            due_date_to_selected_str = datetime.strptime(due_date_to_selected_str, "%d/%m/%Y").strftime("%Y/%m/%d")

            where_str = where_str + "and truck_plan_management_pickup.due_date between '%s' and '%s'" % (due_date_from_selected_str,due_date_to_selected_str)
        
        if supplier_code_selected_str is not None and supplier_code_selected_str != "":
            
            where_str = where_str + " and UPPER(truck_plan_management_pickup.supplier_code) = '%s' " % supplier_code_selected_str.upper()
        
        if PUS_ref_selected_str is not None and PUS_ref_selected_str != "":
            
            PUS_ref_selected_str = "%"+PUS_ref_selected_str+"%"
            where_str = where_str + " and  truck_plan_management_pickup.pickup_no LIKE '%%%s%%'  " %  PUS_ref_selected_str
        
        query = query + joint_str + where_str + group_by + " Order by pickup_no"
        cursor.execute(query)
        result_pickUp_list = cursor.fetchall()
        return_pickUp_list = []

        for pickUp_obj in result_pickUp_list :

            pickUp_serializer_obj = PickUp_Serializer()
            pickUp_serializer_obj.pickup_no = pickUp_obj[0]
            pickUp_serializer_obj.supplier_code = pickUp_obj[1]
            pickUp_serializer_obj.plant_code = pickUp_obj[2]
            pickUp_serializer_obj.due_date = datetime.strptime(pickUp_obj[3].strftime("%Y-%m-%d"), "%Y-%m-%d").date()
            pickUp_serializer_obj.release_time = pickUp_obj[4]
            pickUp_serializer_obj.delivery_time = pickUp_obj[5]
            pickUp_serializer_obj.route_code = pickUp_obj[6]
            pickUp_serializer_obj.route_trip = pickUp_obj[7]
            pickUp_serializer_obj.truck_license = pickUp_obj[8]
            pickUp_serializer_obj.name = pickUp_obj[9]
            pickUp_serializer_obj.order_count = pickUp_obj[10]
            pickUp_serializer_obj.status  = pickUp_obj[11]
            self.csv_list.append((pickUp_obj[0],
                            "Complete" if pickUp_obj[11] == 2 else "Waiting",
                            pickUp_obj[1],
                            pickUp_obj[2],
                            pickUp_obj[11],
                            datetime.strptime(pickUp_obj[3].strftime("%Y-%m-%d"), "%Y-%m-%d").date(),
                            NumberFormat.formal_decimal(pickUp_obj[4]),
                            NumberFormat.formal_decimal(pickUp_obj[5]),
                            pickUp_obj[6],
                            pickUp_obj[7],
                            pickUp_obj[8],
                            pickUp_obj[9],
                            ))

            return_pickUp_list.append(pickUp_serializer_obj)

        return return_pickUp_list


    def search_generate_truck_plan(self,customer_code_selected_str,project_code_selected_str,due_date_selected_str):

        query_first = "select truck_plan_management_truckplan.truckplan_no,COUNT(truck_plan_management_truckplan.truckplan_no),truck_plan_management_pickup.due_date,"
        query_first = query_first + " truck_plan_management_pickup.route_code,truck_plan_management_pickup.route_trip "
        query_first = query_first + " from truck_plan_management_truckplan "

        joint_str_first = " LEFT JOIN truck_plan_management_pickup ON truck_plan_management_pickup.truckplan_no = truck_plan_management_truckplan.truckplan_no "
        where_str_first = " where 1 = 1  and truck_plan_management_pickup.is_active = true and truck_plan_management_pickup.status = 2"

        query_second = "select truck_plan_management_pickup.truckplan_no,COUNT(truck_plan_management_pickup.truckplan_no),truck_plan_management_pickup.due_date,"
        query_second = query_second + " truck_plan_management_pickup.route_code,truck_plan_management_pickup.route_trip "
        query_second = query_second + " from truck_plan_management_pickup "

        joint_str_second  = ""
        where_str_second  = " where 1 = 1  and truck_plan_management_pickup.is_active = true and truck_plan_management_pickup.status = 2 "

        if customer_code_selected_str is not None and customer_code_selected_str != "":
            
            joint_str_first = joint_str_first + " INNER JOIN master_data_routermaster " 
            joint_str_first = joint_str_first + " ON UPPER(master_data_routermaster.route_code) = UPPER(truck_plan_management_pickup.route_code) "
            joint_str_first = joint_str_first + " and UPPER(master_data_routermaster.trip_no) = UPPER(truck_plan_management_pickup.route_trip) "
            
            joint_str_first = joint_str_first + " INNER JOIN master_data_project  "
            joint_str_first = joint_str_first + " ON UPPER(master_data_project.project_code) = UPPER(master_data_routermaster.project_code) "
            
            joint_str_first = joint_str_first + " INNER JOIN master_data_customer "
            joint_str_first = joint_str_first + " ON UPPER(master_data_customer.customer_code) = UPPER(master_data_project.customer_code) "

            where_str_first = where_str_first + " and   UPPER(master_data_customer.customer_code) = '%s' " % customer_code_selected_str.upper()

            joint_str_second = joint_str_second + " INNER JOIN master_data_routermaster " 
            joint_str_second = joint_str_first + " ON UPPER(master_data_routermaster.route_code) = UPPER(truck_plan_management_pickup.route_code) "
            joint_str_second = joint_str_second + " and UPPER(master_data_routermaster.trip_no) = UPPER(truck_plan_management_pickup.route_trip) "

            joint_str_second = joint_str_second + " INNER JOIN master_data_project "
            joint_str_second = joint_str_second + " ON UPPER(master_data_project.project_code) = UPPER(order_order.project_code) "

            joint_str_second = joint_str_second + " INNER JOIN master_data_customer "
            joint_str_second = joint_str_second + " ON UPPER(master_data_customer.customer_code) = UPPER(master_data_project.customer_code) "
                    
            where_str_second = where_str_second + " and   UPPER(master_data_customer.customer_code) = '%s' " % customer_code_selected_str.upper()

        if due_date_selected_str is not None :

            due_date_selected_str = datetime.strptime(due_date_selected_str, "%d/%m/%Y").strftime("%Y/%m/%d")
            where_str_first = where_str_first + "and truck_plan_management_pickup.due_date = '%s' " % due_date_selected_str

            where_str_second = where_str_second + "and truck_plan_management_pickup.due_date = '%s' " % due_date_selected_str

        query_first = query_first + joint_str_first + where_str_first + " GROUP BY truck_plan_management_truckplan.truckplan_no,truck_plan_management_pickup.due_date,truck_plan_management_pickup.route_code,truck_plan_management_pickup.route_trip  "

        query_second = query_second + joint_str_second + where_str_second + " GROUP BY truck_plan_management_pickup.truckplan_no,truck_plan_management_pickup.due_date,truck_plan_management_pickup.route_code,truck_plan_management_pickup.route_trip "
        
        cursor.execute(query_first + " UNION " + query_second )
        result_pickup_list = cursor.fetchall()

        return_pickup_list = []
        self.csv_list = []

        for pickup_obj in result_pickup_list :

            print(pickup_obj[2].strftime("%Y-%m-%d"))
            truckPlan_serializer_obj = TruckPlan_Serializer()
            truckPlan_serializer_obj.truckplan_no = pickup_obj[0]
            truckPlan_serializer_obj.pickUp_count = pickup_obj[1]
            truckPlan_serializer_obj.due_date = datetime.strptime(pickup_obj[2].strftime("%Y-%m-%d"), "%Y-%m-%d").date()
            truckPlan_serializer_obj.route_code = pickup_obj[3]
            truckPlan_serializer_obj.route_trip = pickup_obj[4]

            self.csv_list.append((pickup_obj[0],
                            pickup_obj[0],
                            pickup_obj[1],
                            datetime.strptime(pickup_obj[2].strftime("%Y-%m-%d"), "%Y-%m-%d"),
                            pickup_obj[3],
                            pickup_obj[4]
                            ))

            
            return_pickup_list.append(truckPlan_serializer_obj)
        
        return return_pickup_list


    def search_and_print_truck_plan(self,customer_code_selected_str,project_code_selected_str,due_date_from_selected_str,due_date_to_selected_str,truck_plan_ref):


        query = "SELECT truck_plan_management_truckplan.truckplan_no,"
        query = query + "COUNT(truck_plan_management_pickup.truckplan_no),"
        query = query + "truck_plan_management_truckplan.due_date,"
        query = query + "master_data_routermaster.release_time,"
        query = query + "master_data_routermaster.delivery_time,"
        query = query + "truck_plan_management_truckplan.route_code,"
        query = query + "truck_plan_management_truckplan.route_trip,"
        query = query + "master_data_routerinfo.truck_license,"
        query = query + "master_data_driver.name, "
        query = query + "truck_plan_management_truckplan.status "
        query = query + "FROM public.truck_plan_management_truckplan "

        joint_str =  " LEFT JOIN truck_plan_management_pickup "
        joint_str = joint_str + " ON UPPER(truck_plan_management_pickup.truckplan_no) = UPPER(truck_plan_management_truckplan.truckplan_no) "

        joint_str = joint_str + " LEFT JOIN master_data_routermaster ON "
        joint_str = joint_str + " UPPER(master_data_routermaster.route_code) = UPPER(truck_plan_management_pickup.route_code) and "
        joint_str = joint_str + " UPPER(master_data_routermaster.trip_no) = UPPER(truck_plan_management_pickup.route_trip) "

        joint_str = joint_str + " LEFT JOIN master_data_routerinfo ON "
        joint_str = joint_str + " UPPER(master_data_routerinfo.route_code) = UPPER(master_data_routermaster.route_code) and "
        joint_str = joint_str + " UPPER(master_data_routerinfo.trip_no) = UPPER(master_data_routermaster.trip_no) "

        joint_str = joint_str + " LEFT JOIN master_data_driver ON "
        joint_str = joint_str + " UPPER(master_data_driver.driver_code) = UPPER(master_data_routerinfo.driver_code) "

        group_by_str = "GROUP BY "
        group_by_str = group_by_str + " truck_plan_management_truckplan.truckplan_no,"
        group_by_str = group_by_str + " truck_plan_management_truckplan.due_date,"
        group_by_str = group_by_str + " master_data_routermaster.release_time,"
        group_by_str = group_by_str + " master_data_routermaster.delivery_time,"
        group_by_str = group_by_str + " truck_plan_management_truckplan.route_code,"
        group_by_str = group_by_str + " truck_plan_management_truckplan.route_trip,"
        group_by_str = group_by_str + " master_data_routerinfo.truck_license,"
        group_by_str = group_by_str + " master_data_driver.name,"
        group_by_str = group_by_str + " truck_plan_management_truckplan.status"

        where_str = " where 1 = 1 "

        if customer_code_selected_str is not None and customer_code_selected_str != "":

            joint_str = joint_str + " left join master_data_project "
            joint_str = joint_str + " ON  UPPER(master_data_project.project_code) = UPPER(master_data_routermaster.project_code) "
            joint_str = joint_str + " left join master_data_customer "
            joint_str = joint_str + " ON UPPER(master_data_customer.customer_code) =  UPPER(master_data_project.customer_code) "

            where_str = where_str + " and UPPER(master_data_customer.customer_code) = '%s' " % customer_code_selected_str.upper()
        
        if project_code_selected_str is not None and project_code_selected_str != "":

            where_str = where_str + " and   UPPER(master_data_routermaster.project_code) = '%s' " % project_code_selected_str.upper()

        if due_date_from_selected_str is not None and due_date_to_selected_str is None:

            due_date_from_selected_str = datetime.strptime(due_date_from_selected_str, "%d/%m/%Y").strftime("%Y/%m/%d")
            where_str = where_str + "and truck_plan_management_truckplan.due_date  >= '%s' " % due_date_from_selected_str
        
        if due_date_from_selected_str is  None and due_date_to_selected_str is not None:

            due_date_to_selected_str = datetime.strptime(due_date_to_selected_str, "%d/%m/%Y").strftime("%Y/%m/%d")
            where_str = where_str + "and truck_plan_management_truckplan.due_date <= '%s' " % due_date_to_selected_str

        if due_date_from_selected_str is not None and due_date_to_selected_str is not None:

            due_date_from_selected_str = datetime.strptime(due_date_from_selected_str, "%d/%m/%Y").strftime("%Y/%m/%d")
            due_date_to_selected_str = datetime.strptime(due_date_to_selected_str, "%d/%m/%Y").strftime("%Y/%m/%d")

            where_str = where_str + "and truck_plan_management_truckplan.due_date between '%s' and '%s'" % (due_date_from_selected_str,due_date_to_selected_str)
        
        if truck_plan_ref is not None and truck_plan_ref != "":
            
            truck_plan_ref = "%"+truck_plan_ref+"%"
            where_str = where_str + " and  truck_plan_management_truckplan.truckplan_no LIKE '%%%s%%'  " %  truck_plan_ref
        
        query = query + joint_str + where_str + group_by_str + " Order by truckplan_no"
        cursor.execute(query)
        result_truckPlan_list = cursor.fetchall()
        return_truckPlan_list = []
        self.csv_list = []

        for truckPlan_obj in result_truckPlan_list :

            truckPlan_serializer_obj = TruckPlan_Serializer()
            truckPlan_serializer_obj.truckplan_no = truckPlan_obj[0]
            truckPlan_serializer_obj.pickUp_count = truckPlan_obj[1]
            truckPlan_serializer_obj.due_date = datetime.strptime(truckPlan_obj[2].strftime("%Y-%m-%d"), "%Y-%m-%d").date()
            truckPlan_serializer_obj.release_time = truckPlan_obj[3]
            truckPlan_serializer_obj.delivery_time = truckPlan_obj[4]
            truckPlan_serializer_obj.route_code = truckPlan_obj[5]
            truckPlan_serializer_obj.route_trip = truckPlan_obj[6]
            truckPlan_serializer_obj.truck_license = truckPlan_obj[7]
            truckPlan_serializer_obj.name = truckPlan_obj[8]  
            truckPlan_serializer_obj.status = truckPlan_obj[9]    

            self.csv_list.append((
                            truckPlan_obj[0],
                            "Complete" if truckPlan_obj[9] == 2 else "Waiting",
                            truckPlan_obj[1],
                            datetime.strptime(truckPlan_obj[2].strftime("%Y-%m-%d"), "%Y-%m-%d").date(),
                            truckPlan_obj[3],
                            truckPlan_obj[4],
                            truckPlan_obj[5],
                            truckPlan_obj[6],
                            truckPlan_obj[7],
                            truckPlan_obj[8] 
                            ))

            return_truckPlan_list.append(truckPlan_serializer_obj)

        return return_truckPlan_list
        

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

        
