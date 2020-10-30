import os 

class FileManagement:

    part = ""

    def __init__(self,part):

        self.part = part
    

    def remove_file(self) :

        os.remove(self.part)


       
    