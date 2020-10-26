from truck_plan_management.models import PickUp,TruckPlan
import math  


class GenerateTruckPlan:

    route_code = ""
    route_trip = ""
    due_date = ""
    letter_list = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

    def __init__(self,route_code,route_trip,due_date):

        self.route_code = route_code
        self.route_trip = route_trip
        self.due_date = due_date

    def route_code_format(self):

        if len(self.route_code) < 3 :
            
            for num in range( 3 - len(self.route_code) ) :

                self.route_code = self.route_code + "_"
            
            return self.route_code 
        else :

            return self.route_code[0:3]
    
    def route_trip_format(self):

        if len(self.route_trip) < 3 :
            
            for num in range( 3 - len(self.route_trip) ) :

                self.route_trip = self.route_trip + "_"
            
            return self.route_trip 
        else :

            return self.route_trip[0:3]
    
    def generate_running_no(self,search):

        truckPlan_count_int = TruckPlan.objects.filter(
            truckplan_no__contains=search
            ).count()

        letter_str = self.letter_list[math.floor(truckPlan_count_int / 99)] 

        return letter_str + "{0:0=2d}".format(truckPlan_count_int + 1)


    def generate_truck_plan(self):

        truck_plan_no = ""
        
        truck_plan_no = truck_plan_no + self.route_code_format() + self.route_trip_format() + self.due_date
        truck_plan_no = truck_plan_no + self.generate_running_no(truck_plan_no )

        return truck_plan_no







    
    

       