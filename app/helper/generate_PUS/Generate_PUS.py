from truck_plan_management.models import PickUp


class Genetate_PUS:

    supplier = ""
    due_date = ""

    def __init__(self,supplier,due_date):

        self.supplier = supplier
        self.due_date = due_date

    def supplier_format(self):

        if len(self.supplier) < 6 :
            
            for num in range( 6 - len(self.supplier) ) :

                self.supplier = self.supplier + "_"
            
            return self.supplier 
        
        return self.supplier 
    
    def generate_running_no(self,search):

        pickUp_count_int = PickUp.objects.filter(
            pickup_no__contains=search
            ).count()
        
        print(pickUp_count_int)

        return "{0:0=2d}".format(pickUp_count_int + 1)


    def generate_PUS(self):

        pickup_no = ""
        
        pickup_no = pickup_no + self.supplier_format() + self.due_date 

        pickup_no = pickup_no + self.generate_running_no(pickup_no )

        return pickup_no







    
    

       