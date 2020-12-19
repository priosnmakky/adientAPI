import openpyxl 
from openpyxl.utils import get_column_letter

class WorkbookHelper:


    @staticmethod
    def read_workbook(file_url_str) :

        workbook_obj = openpyxl.load_workbook(file_url_str)
        sheet_obj = workbook_obj.active

        return sheet_obj



    
        