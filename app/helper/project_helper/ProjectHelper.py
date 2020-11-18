from master_data.serializers import Project_Serializer
from datetime import datetime
from decimal import Decimal
import math

class ProjectHepler:

    
    @staticmethod
    def covert_data_list_to_serializer_list(project_list) :

        project_return_list = []

        for project_obj in project_list :

            project_Serializer = Project_Serializer()
            project_Serializer.project_code = project_obj[0]
            project_Serializer.customer_code = project_obj[1]
            project_Serializer.remark = project_obj[2]
            project_Serializer.updated_by = project_obj[3]
            project_Serializer.updated_date = project_obj[4]

            project_return_list.append(project_Serializer)
        
        return project_return_list
    
    @staticmethod
    def covert_data_list_to_CSV_list(project_list) :

        project_return_list = []

        for project_obj in project_list :

            project_return_list.append([
                project_obj[0],
                project_obj[1],
                project_obj[2],
                project_obj[3],
                project_obj[4].strftime("%d/%m/%Y")

            ])
        
        return project_return_list

    