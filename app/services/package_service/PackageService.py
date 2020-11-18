from order.models import Order
from django.db import connection
from order.serializers import OrderSerializer

cursor = connection.cursor()
class PackageService:


    def search_package (self,customer_code,project_code,supplier_code,package_code,package_no):
 
        cursor = connection.cursor()
        cursor.execute(" Begin;  SELECT * FROM search_package(%s,%s,%s,%s,%s);",[customer_code,project_code,supplier_code,"%"+ package_code + "%","%"+ package_no + "%"]  )

        package_list = cursor.fetchall()
        cursor.close();

        return package_list

    
        
