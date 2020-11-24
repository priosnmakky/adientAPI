import csv

class CSVFileManagement:

    name = ""
    part = ""
    delimiter = ""
    data_list = []
    csv_list = []
    
    def __init__(self,name,part,newline,delimiter):

        self.name = name
        self.part = part
        self.newline = newline
        self.delimiter = delimiter
        self.csv_list = []

    def covert_to_header(self,header_list,) :

        return_header_list = []
        for header in header_list :

            return_header_list.append(header)

        self.csv_list.insert(0, return_header_list
                )
        
        return return_header_list;


    def covert_to_CSV_data_list(self,data_list) :

        for data in data_list :
            
            self.csv_list.append(data)
        
        return self.csv_list

    def genearete_CSV_file(self) :

        CSV_file_name_str = self.name +'.csv'
        with open(self.part +  CSV_file_name_str, 'w', newline=self.newline,encoding='utf-8-sig') as file:
            writer = csv.writer(file, delimiter=self.delimiter, quotechar="'")
            writer.writerows(self.csv_list)
        
        return CSV_file_name_str
    
    @staticmethod
    def read_CSV_file(name_file_str,delimiter,quotechar) :

        with open(name_file_str, newline='') as csvfile:

            data_list = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar)

        
        return data_list
    

            


    
        