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

    # def search_pending_order (self,customer_code,project_code,supplier_code,plant_code,start_date,end_date):
        
    #     cursor = connection.cursor()
    #     cursor.execute(" Begin;  SELECT * FROM search_pending_order(%s,%s,%s,%s,%s,%s);",[customer_code,project_code,supplier_code,plant_code,start_date,end_date]  )

    #     order_list = cursor.fetchall()
    #     cursor.close();

    #     return order_list
    
    # def search_upload_order_log_file (self,customer_code,project_code,start_date,end_date):
     
    #     cursor = connection.cursor()
    #     cursor.execute(" Begin;  SELECT * FROM search_upload_order_log_file(%s,%s,%s,%s);",[customer_code,project_code,start_date,end_date]  )

    #     file_list = cursor.fetchall()
    #     cursor.close();

    #     return file_list

    # def search_order_transaction (self,customer_code,project_code,file_no,order_no,supplier_code,plant_code,start_date,end_date):
        
    #     cursor = connection.cursor()
    #     cursor.execute(" Begin;  SELECT * FROM search_order_transaction(%s,%s,%s,%s,%s,%s,%s,%s);",[customer_code,project_code,file_no,order_no,supplier_code,plant_code,start_date,end_date]  )

    #     order_list = cursor.fetchall()
    #     cursor.close();

    #     return order_list
    
        
