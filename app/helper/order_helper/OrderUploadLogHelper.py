from order.serializers import FileSerializer
from datetime import datetime
from decimal import Decimal
import math
from app.helper.config.ConfigPart import ConfigPart
from app.helper.file_management.FileManagement import FileManagement

configPart = ConfigPart()

class OrderUploadLogHelper:

    
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
            fileSerializer.csv_url = FileManagement.find_file(configPart.configs.get("UPLOAD_ORDER_PART").data,file_obj[2]+".csv")

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

    