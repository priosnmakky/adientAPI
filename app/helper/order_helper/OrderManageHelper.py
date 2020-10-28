from order.models import Order
import json
from app.helper.order_helper.OrderUploadHelper import OrderUploadHelper
from order.model.order_history import order_history

class OrderManageHelper:

    order_list = []
    order_csv_list = []
    order_csv_list_database = []
    order_db_list = []
    due_date_list = []
    file_no = ""


    def __init__(self,file_no,order_list,due_date_list):

        self.file_no = file_no
        self.order_list = order_list
        self.due_date_list = due_date_list
        
    
    def get_order_db(self) :
        
        self.order_db_list = set(Order.objects.filter(is_deleted=False).values_list("part_number","supplier_no","plant_no","due_date__year","due_date__month","due_date__day","order_id","order_qty","history_updated"))
        order_database_set = set([(db[0].upper(),db[1].upper(),db[2].upper(),db[3],db[4],db[5]) for db in self.order_db_list ])
        
        return order_database_set
 
    
    def get_order_workbook(self) :

        order_workbook_set = set([wb[3] for wb in self.order_list if wb[2] > 5 and  str(wb[0]).isnumeric() and int(str(wb[0])) >0 ] )

        return order_workbook_set
    
    def get_order_history(self,order_qry,history_obj,action) :

        order_history_obj = order_history()

        if action == "ADD" :

            order_history_obj.add = order_qry
            order_history_obj.update = []
            order_history_obj.delete = []

        if action == "UPDATE" :
            
            history_updated_obj = json.loads(history_obj)
            history_updated_obj['update'].append(order_qry)
            order_history_obj.update = history_updated_obj['update'].append(order_qry)

        if action == "DELETE" :
            
            history_updated_obj = json.loads(history_obj)
            history_updated_obj['delete'].append(order_qry)
            order_history_obj.update = history_updated_obj['update'].append(order_qry)
            
        history_str = json.dumps( order_history_obj.__dict__ )

        return history_str
        
    
    def add_order_cvs(self,item_no,order_no,part_number,supplier_code,plant_code,order_qty,due_date) :

        self.order_csv_list.append(
            (
            item_no,#Item_no
            order_no,#order_no
            part_number, #part_number
            order_qty, #order_qty
            supplier_code, # supplier_code
            plant_code,# plant_code
            order_qty,#order_qty
            due_date.strftime("%d/%m/%Y") #due_date 
            )
        )

        return self.order_csv_list

    def add_order_cvs_database(self,item_no,part_number,file_no,order_no,due_date,order_qry,history_str,supplier_code,plant_code,part_name,action) :

        self.order_csv_list_database.append(
            (
            item_no, #Item_no
            part_number, #part_number
            file_no, #file_no
            order_no, #order_id
            "" if due_date == "" else due_date.strftime("%d/%m/%Y"), #due_date 
            order_qry, #order_qty
            history_str, #history_str
            supplier_code, # supplier_no
            plant_code, # plant_no
            part_name, # part_name,
            action
            )
        )

        return self.order_csv_list_database
    
    def add_order(self,order_obj) :

        order_no = OrderUploadHelper.generate_order_no([d[1] for d in self.due_date_list if d[0] == order_obj[4][5]][0],order_obj[4][5].strftime("%Y%m%d"))
        history_str = self.get_order_history(order_obj[0],None,"ADD")

        self.add_order_cvs_database(
            order_obj[4][0],#Item_no
            order_obj[4][1],#part_number
            self.file_no,#file_no
            order_no,#order_no
            order_obj[4][5],#due_date 
            order_obj[0],#order_qty
            history_str,#history_str
            order_obj[4][3],# supplier_code
            order_obj[4][4],# plant_code
            order_obj[4][2],# part_name
            "add"
        )

        self.add_order_cvs(
            order_obj[4][0],#Item_no
            order_no,#order_id
            order_obj[4][1], #part_number
            order_obj[4][3], # supplier_code
            order_obj[4][4],# plant_code
            order_obj[0],#order_qty
            order_obj[4][5] #due_date 
        )

        return self.order_csv_list_database
    
    def update_order(self,order_obj) :

        order_in_db_list = [o for o in self.order_db_list if  {o[0].upper(),o[1].upper(),o[2].upper(),o[3],o[4],o[5]} == set(order_obj[3])  ]
            
        if len(order_in_db_list) > 0 and int(order_in_db_list[0][7]) !=  int(order_obj[0]):
                    
            history_str = self.get_order_history(order_in_db_list[0][7],order_in_db_list[0][8],"UPDATE")

            self.add_order_cvs_database(
                order_obj[4][0],#Item_no
                order_obj[4][1],#part_number
                self.file_no,#file_no
                order_in_db_list[0][6],#order_no
                order_obj[4][5],#due_date 
                order_obj[0],#order_qty
                history_str,#history_str
                order_obj[4][3],# supplier_code
                order_obj[4][4],# plant_code
                order_obj[4][2],# part_name
                "update"
            )

        self.add_order_cvs(
            
            order_obj[4][0],#Item_no
            order_in_db_list[0][6],#order_id
            order_obj[4][1], #part_number
            order_obj[4][3], # supplier_code
            order_obj[4][4],# plant_code
            order_obj[0],#order_qty
            order_obj[4][5] #due_date 
        )

        return self.order_csv_list_database
    
    def delete_order(self,delete_order_obj):

        history_str = self.get_order_history(delete_order_obj[7],delete_order_obj[8],"DELETE")

        self.add_order_cvs_database(
                "",#Item_no
                "",#part_number
                self.file_no,#file_no
                delete_order_obj[6],#order_no
                "",#due_date 
                "",#order_qty
                history_str,#history_str
                "",# supplier_code
                "",# plant_code
                "",# part_name
                "delete"
            )

        return self.order_csv_list_database
    
    def order_management(self) : 

        order_management_list = [o for o in self.order_list if   (o[2] > 5 and int(o[0]) > 0 )]

        for  order_obj in order_management_list :

            if  not order_obj[3] in self.get_order_db(): 

                # order_no = self.generate_order_no([d[1] for d in self.due_date_list if d[0] == order_obj[4][5]][0],order_obj[4][5].strftime("%Y%m%d"))
                # history_str = self.get_order_history(order_obj[0],None,"ADD")

                self.add_order(order_obj)
            
            else :
                
                self.update_order(order_obj)
        
        delete_order_list = [o for o in self.order_db_list if (o[0].upper(),o[1].upper(),o[2].upper(),o[3],o[4],o[5]) not in self.get_order_workbook()  ]
            
        for delete_order in delete_order_list :   

            self.delete_order(delete_order)
            
                    
                    



        

 