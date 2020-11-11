from datetime import datetime
from decimal import Decimal
from order.model.order_transaction import Order_transaction
import math
import json

class OrderTransactionHelper:

    order_transaction_list = []
    order_CSV_list = []

    def __init__(self):

        self.order_transaction_list = []


    def add_order_transaction(self,history_obj,order_obj) :

        order_transaction_obj = Order_transaction()
        order_transaction_obj.action = 'ADD'
        order_transaction_obj.file_no = order_obj[1]
        order_transaction_obj.order_no = order_obj[2]
        order_transaction_obj.supplier_code = order_obj[3]
        order_transaction_obj.plant_code = order_obj[4]
        order_transaction_obj.part_number = order_obj[5]

        order_transaction_obj.part_name = order_obj[6]

        order_transaction_obj.due_date = order_obj[7]
        order_transaction_obj.order_qty = int(history_obj['add'])

        if order_obj[9] == None or order_obj[9] == "":

            order_transaction_obj.package_no = None
            order_transaction_obj.package_qty = None
            order_transaction_obj.route_trip = None
                
        else : 

            order_transaction_obj.package_no = order_obj[9]
            order_transaction_obj.package_qty = order_obj[10]
            order_transaction_obj.route_trip = order_obj[12]

        order_transaction_obj.updated_by = order_obj[13]
        order_transaction_obj.updated_date = order_obj[14]

        self.add_CSV('ADD',
                order_obj[1],
                order_obj[2],
                order_obj[3],
                order_obj[4],
                order_obj[5],
                order_obj[6],
                order_obj[7],
                int(history_obj['add']),
                order_obj[9],
                order_obj[10],
                order_obj[12],
                order_obj[13],
                order_obj[14]
                )
        

        return order_transaction_obj


    def update_order_transaction(self,history_obj,order_obj) :

        order_transaction_list = []
        for history_update_obj in history_obj['update'] :
            
            order_transaction_obj = Order_transaction()
            order_transaction_obj.action = 'UPDATE'
            order_transaction_obj.file_no = order_obj[1]
            order_transaction_obj.order_no = order_obj[2]
            order_transaction_obj.supplier_code = order_obj[3]
            order_transaction_obj.plant_code = order_obj[4]
            order_transaction_obj.part_number = order_obj[5]
            order_transaction_obj.part_name = order_obj[6]
            order_transaction_obj.due_date = order_obj[7]
            order_transaction_obj.order_qty = int(history_update_obj)

            if order_obj[9] == None or order_obj[9]== "":

                order_transaction_obj.package_no = None
                order_transaction_obj.package_qty = None
                order_transaction_obj.route_trip = None
                    
            else : 

                order_transaction_obj.package_no = order_obj[9]
                order_transaction_obj.package_qty = order_obj[10]
                order_transaction_obj.route_trip = order_obj[12]

            order_transaction_obj.updated_by = order_obj[13]
            order_transaction_obj.updated_date = order_obj[14]

            order_transaction_list.append(order_transaction_obj)

            self.add_CSV('UPDATE',
                order_obj[1],
                order_obj[2],
                order_obj[3],
                order_obj[4],
                order_obj[5],
                order_obj[6],
                order_obj[7],
                int(history_update_obj),
                order_obj[9],
                order_obj[10],
                order_obj[12],
                order_obj[13],
                order_obj[14]
                )

        return order_transaction_list
    

    def delete_order_transaction(self,history_obj,order_obj) :

        order_transaction_list = []

        for history_delete_obj in history_obj['delete'] :

            order_transaction_obj = Order_transaction()
            order_transaction_obj.action = 'DELETE'
            order_transaction_obj.file_no = order_obj[1]
            order_transaction_obj.order_no = order_obj[2]
            order_transaction_obj.supplier_code = order_obj[3]
            order_transaction_obj.plant_code = order_obj[4]
            order_transaction_obj.part_number = order_obj[5]
            order_transaction_obj.part_name = order_obj[6]
            order_transaction_obj.due_date = order_obj[7]
            order_transaction_obj.order_qty = int(history_delete_obj)
                    
            if order_obj[9] == None or order_obj[9] == "":

                order_transaction_obj.package_no = None
                order_transaction_obj.package_qty = None
                order_transaction_obj.route_trip = None
                
            else : 

                order_transaction_obj.package_no = order_obj[9]
                order_transaction_obj.package_qty = order_obj[10]
                order_transaction_obj.route_trip = order_obj[12]
    
            order_transaction_obj.updated_by = order_obj[13]
            order_transaction_obj.updated_date = order_obj[14]

            self.add_CSV('DELETE',
                order_obj[1],
                order_obj[2],
                order_obj[3],
                order_obj[4],
                order_obj[5],
                order_obj[6],
                order_obj[7],
                int(history_delete_obj),
                order_obj[9],
                order_obj[10],
                order_obj[12],
                order_obj[13],
                order_obj[14]
                )

            order_transaction_list.append(order_transaction_obj)

        return order_transaction_list
        
    def transaction_management(self,order_list) :

        for order_obj in order_list :

            history_obj = json.loads(order_obj[0]) 

            add_order_obj = self.add_order_transaction(history_obj,order_obj)

            self.order_transaction_list.append(add_order_obj)

            update_order_transaction_list = self.update_order_transaction(history_obj,order_obj)

            self.order_transaction_list.extend(update_order_transaction_list)

            delete_order_transaction_list = self.delete_order_transaction(history_obj,order_obj)
            
            self.order_transaction_list.extend(delete_order_transaction_list)
        
        return self.order_transaction_list
    
    def add_CSV(self,action,file_no,order_no,supplier_code,plant_code,part_number,part_name,due_date,order_qty,package_no,package_qty,route_trip,updated_by,updated_date) :

        self.order_CSV_list.append([action,
            file_no,
            order_no,
            supplier_code,
            plant_code,
            part_number,
            part_name,
            due_date.strftime("%d/%m/%Y") ,
            order_qty,
            package_no,
            package_qty,
            route_trip,
            updated_by,
            updated_date.strftime("%d/%m/%Y")])

        return self.order_CSV_list


    @staticmethod
    def covert_data_list_to_serializer_list(file_list) :

        file_return_list = []

        for file_obj in file_list :

            fileSerializer = FileSerializer()
            fileSerializer.customer_code = file_obj[0]
            fileSerializer.project_code = file_obj[1]
            fileSerializer.file_no = file_obj[2]
            fileSerializer.order_count = file_obj[3]
            fileSerializer.status = file_obj[4]
            fileSerializer.updated_by = file_obj[5]
            fileSerializer.updated_date = file_obj[6]

            file_return_list.append(fileSerializer)
        
        return file_return_list
    
    @staticmethod
    def covert_data_list_to_CSV_list(file_list) :

        file_return_list = []

        for file_obj in file_list :

            file_return_list.append([
                file_obj[0],
                file_obj[1],
                file_obj[2],
                file_obj[3],
                'Confirm' if file_obj[3] == 2 else 'Draft',
                file_obj[5],
                file_obj[6].strftime("%d/%m/%Y")

            ])
        
        return file_return_list

    