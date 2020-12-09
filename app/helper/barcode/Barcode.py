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

        
