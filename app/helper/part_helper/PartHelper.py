from master_data.serializers import Part_Serializer
from datetime import datetime
from decimal import Decimal
import math

class PartHelper:

    
    @staticmethod
    def covert_data_list_to_serializer_list(part_list) :

        part_return_list = []

        for part_obj in part_list :

            part_Serializer = Part_Serializer()
            part_Serializer.project_code = part_obj[0]
            part_Serializer.status = part_obj[1]
            part_Serializer.supplier_code = part_obj[2]
            part_Serializer.part_number = part_obj[3]
            part_Serializer.part_name = part_obj[4]
            part_Serializer.package_no = part_obj[5]
            part_Serializer.package_volume = part_obj[6]
            part_Serializer.package_weight = part_obj[7]
            part_Serializer.remark = part_obj[8]
            part_Serializer.updated_by = part_obj[9]
            part_Serializer.updated_date = part_obj[10]

            part_return_list.append(part_Serializer)
        
        return part_return_list
    
    @staticmethod
    def covert_data_list_to_CSV_list(part_list) :

        part_return_list = []

        for part_obj in part_list :

            part_return_list.append([
                part_obj[0],
                "Draft" if part_obj[1] == 1 else "Confirm" ,
                part_obj[2],
                part_obj[3],
                part_obj[4],
                part_obj[5],
                part_obj[6],
                part_obj[7],
                part_obj[8],
                part_obj[9],
                part_obj[10].strftime("%d/%m/%Y")
            ])
        
        return part_return_list

    