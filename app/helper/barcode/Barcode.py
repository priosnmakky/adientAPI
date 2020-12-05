import code128
from app.helper.config.ConfigPart import ConfigPart
from app.helper.file_management.FileManagement import FileManagement

configPart = ConfigPart()

class Barcode:

    name = ""
   
    
    def __init__(self,name):

        self.name = name
 
    def generate_code128(self,part,data):    
        

        code128.image(data).save(part + self.name +".png")  # with PIL present

        

    # def generate_barcode(self,data):
    #     print(data)
    #     barcode_obj = CODE128(data, writer=ImageWriter())
    #     barcode_obj.save("pdf/static/"+self.name)
    

   

    

        # with open("media/" +  self.name +'.csv', 'w', newline='',encoding='utf-8') as file:
        #     writer = csv.writer(file)
        #     writer.writerows(part_csv_list)


    
        