
from io import BytesIO
from xhtml2pdf import pisa
from order.models import Order



class PDFManagement:

    name = ""
    part = ""
    data_list = []
    csv_list = []
    
    def __init__(self):
        pass

    @staticmethod
    def generate_pdf(html_srt,name_pdf_str,link_callback) :

        write_to_file = open(name_pdf_str, "w+b")
        result = pisa.CreatePDF(html_srt.encode('utf-8'),dest=write_to_file,link_callback=link_callback,encoding='utf-8-sig', html_encoding="utf-8-sig")
                
        write_to_file.close()

        return True
                
        


    def covert_to_CSV_data_list(self,data_list) :

        for data in data_list :
            
            self.csv_list.append(data)
        
        return self.csv_list

    def genearete_CSV_file(self) :

        CSV_file_name_str = self.name +'.csv'
        with open(self.part +  CSV_file_name_str, 'w', newline=self.newline,encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerows(self.csv_list)
        
        return CSV_file_name_str


    
        