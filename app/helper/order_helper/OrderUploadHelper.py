from master_data.models import Customer
from order.models import File,Order
from datetime import datetime,timedelta

class OrderUploadHelper:

    today_date_str = datetime.utcnow().strftime("%y%m%d")
    partNumber_list = []
    partDescription_list = []
    supplierName_list = []
    plantName_list = []
    due_date_list = []
    
    def __init__(self):
        pass

    @staticmethod
    def generate_file_no(customer_id) :

        today_date_str = datetime.utcnow().strftime("%y%m%d")
        customer_code_str = Customer.objects.get(customer_code = customer_id ).customer_code
        customer_code_2dg_first_start_str = customer_code_str[0:2]
        file_count = File.objects.filter(file_no__contains= today_date_str ).count()
        print(file_count)
        file_no = customer_code_2dg_first_start_str + today_date_str + "{0:0=2d}".format(file_count + 1)

        return file_no
    
    @staticmethod
    def generate_order_no(amount,due_date_str):

        letter_list = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        amount = amount + 1
        no_str = due_date_str 
        amount_letter_int = int(amount/1000)
        amount_minus_letter_int =  amount  % 1000 

        
        if amount_minus_letter_int == 0:

            no_str = no_str + letter_list[amount_letter_int ] + "001"
        
        else :

            order_number_str = str(amount)

            if amount > 1000 :

                amount_minus_letter_int = amount_minus_letter_int + 1

            if amount_minus_letter_int < 10:

                order_number_str = "00" + str(amount_minus_letter_int ) 

            elif amount_minus_letter_int < 100:

                order_number_str = "0" + str(amount_minus_letter_int )
            
            no_str = no_str + letter_list[amount_letter_int ] + order_number_str

        return no_str
    
    
    @staticmethod
    def data_mapping_from_sheet(sheet_obj) :

        order_list = []
        partNumber_list = []
        partDescription_list = []
        supplierName_list = []
        plantName_list = []
        due_date_list = []
        


        for row_int in range(3,sheet_obj.max_row + 1):

            order_column = []

            for column_int in range(1,sheet_obj.max_column +1 ): 

                order_data_str =  sheet_obj.cell(row=row_int, column=column_int).value 
                
                if order_data_str != None or sheet_obj.cell(row=2, column=column_int).value != None:
                    
                    order_data_str ="" if order_data_str == None  else order_data_str
                    
                    if column_int == 1 :
                        
                        order_list.append((str(order_data_str),row_int,column_int))
                    
                    if column_int == 2 :

                        partNumber_list.append(str(order_data_str))
                        order_list.append((str(order_data_str),row_int,column_int))
                    
                    elif column_int == 3 :

                        partDescription_list.append(str(order_data_str))
                        order_list.append((str(order_data_str),row_int,column_int))
                    
                    elif column_int == 4 :

                        supplierName_list.append(str(order_data_str))
                        order_list.append((str(order_data_str),row_int,column_int))

                    elif column_int == 5 :

                        plantName_list.append(str(order_data_str))
                        order_list.append((str(order_data_str),row_int,column_int))
                    
 
                    elif column_int > 6 :

                            due_date_datetime = sheet_obj.cell(row=2, column=column_int).value
                            time_datetime = sheet_obj.cell(row=row_int, column=6).value
                            due_date_datetime = datetime.combine(due_date_datetime,time_datetime)
                            due_date_datetime = due_date_datetime - timedelta(hours=7)
                   
                            if not due_date_datetime in [ d[0] for d in due_date_list] :

                                due_date_db_list = Order.objects.filter(
                                    due_date__year= due_date_datetime.year,
                                    due_date__month=due_date_datetime.month,
                                    due_date__day=due_date_datetime.day,
                                    ).values_list("due_date__day")

                                due_date_list.append((due_date_datetime,len(due_date_db_list)) )

                            order_list.append((str(order_data_str),row_int,column_int,(
                                str(sheet_obj.cell(row=row_int, column=2).value) if str(sheet_obj.cell(row=row_int, column=2).value).isnumeric() else str(sheet_obj.cell(row=row_int, column=2).value).upper(),
                                str(sheet_obj.cell(row=row_int, column=4).value) if str(sheet_obj.cell(row=row_int, column=4).value).isnumeric() else str(sheet_obj.cell(row=row_int, column=4).value).upper(),
                                str(sheet_obj.cell(row=row_int, column=5).value) if str(sheet_obj.cell(row=row_int, column=5).value).isnumeric() else str(sheet_obj.cell(row=row_int, column=5).value).upper(),
                                due_date_datetime.year,
                                due_date_datetime.month,
                                due_date_datetime.day
                                ),
                                (
                                    str(sheet_obj.cell(row=row_int, column=1).value),
                                    str(sheet_obj.cell(row=row_int, column=2).value),
                                    str(sheet_obj.cell(row=row_int, column=3).value),
                                    str(sheet_obj.cell(row=row_int, column=4).value),
                                    str(sheet_obj.cell(row=row_int, column=5).value),
                                    due_date_datetime
                                )
                                ))
        
        return (order_list,partNumber_list,partDescription_list,supplierName_list,plantName_list,due_date_list)




    
        