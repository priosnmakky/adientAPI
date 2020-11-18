import os 
from django.core.files.storage import FileSystemStorage

class FileManagement:

    part = ""

    def __init__(self,part):

        self.part = part
    
    def save_file(self,image_name_str,image_obj):

        try: 

            fs = FileSystemStorage(location=self.part) #defaults to   MEDIA_ROOT  
            file_name_str = fs.save(image_name_str, image_obj)

            return image_name_str

        except:
            
            print("test")
            return ""
    

    def remove_file(self) :

        os.remove(self.part)


       
    