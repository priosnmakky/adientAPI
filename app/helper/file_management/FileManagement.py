import os 
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from datetime import datetime

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

            return ""
    

    def remove_file(self) :

        os.remove(self.part)
    
    
    
    
    @staticmethod
    def validate_folder(folder_part) :

        now_datetime = datetime.utcnow()
        
        now_str = "/"+ datetime.utcnow().strftime("%d-%m-%Y")
        part_str = settings.MEDIA_ROOT + "/"+folder_part + now_str

        if not os.path.exists(part_str):
            
            os.makedirs(part_str)

        return folder_part + now_str
    
    @staticmethod
    def find_file(root_folder,file_name) :

        for root, dirs, files in os.walk(settings.MEDIA_ROOT+"\\" +root_folder ):
            if file_name in files:
                folder_list = root.split('\\')
                dir_str = folder_list[len(folder_list)-1]

                return  root_folder+'/'+dir_str+"/"+ file_name
        

        return ""
        


    




       
    
