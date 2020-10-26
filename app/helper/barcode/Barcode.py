import code128

class Barcode:

    name = ""
   
    
    def __init__(self,name):

        self.name = name
 
    def generate_code128(self,data):
        
        code128.image(data).save("pdf/static/" + self.name +".png")  # with PIL present

    # def generate_barcode(self,data):
    #     print(data)
    #     barcode_obj = CODE128(data, writer=ImageWriter())
    #     barcode_obj.save("pdf/static/"+self.name)
    

   

    

        # with open("media/" +  self.name +'.csv', 'w', newline='',encoding='utf-8') as file:
        #     writer = csv.writer(file)
        #     writer.writerows(part_csv_list)


    
        