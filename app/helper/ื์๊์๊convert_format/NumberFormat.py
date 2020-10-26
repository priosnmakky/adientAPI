class NumberFormat:

    @staticmethod
    def formal_decimal(number_str):

    number_array = number_str.split(".")

    print(number_array)
    if len(number_array[0]) == 1 :

        number_array[0] =  "0" + number_array[0] 

    if len(number_array[1]) == 1 :

        number_array[1] =  number_array[1] +"0" 

    return number_array[0] +"."+ number_array[1]







    
    

       