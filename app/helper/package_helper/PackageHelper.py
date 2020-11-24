from master_data.serializers import Package_Serializer
from master_data.models import Package
from datetime import datetime
from decimal import Decimal
import math
from app.helper.config.ConfigMessage import ConfigMessage


configMessage = ConfigMessage()

class PackageHelper:

    massage_error = ""


    def validate_station_code(self,station_code):

        if station_code == None or station_code == "" :
        
            self.massage_error = configMessage.configs.get("PACKAGES_MASTER_STATIONCODE_REQUIRED").data

            return False
        
        return True
    
    def validate_package_code(self,package_code):

        if package_code == None or package_code == "" :

            self.massage_error = configMessage.configs.get("PACKAGES_MASTER_PACKAGECODE_REQUIRED").data

            return False
        
        return True
    
    def validate_package_no(self,package_no):

        package_list = Package.objects.filter(package_no=package_no,is_active=True)

        if package_no == None or package_no == "" :

            self.massage_error = configMessage.configs.get("PACKAGES_MASTER_PACKAGENO_REQUIRED").data

            return False
        
        elif  len(package_list) > 0 :

            self.massage_error = configMessage.configs.get("PACKAGES_MASTER_DUPLICATE").data

            return False

        return True
    
    def validate_snp(self,snp):

        if snp == None or snp == "" :

            self.massage_error = configMessage.configs.get("PACKAGES_MASTER_SNP_REQUIRED").data

            return False
        
        elif int(snp) <= 0 :

            self.massage_error  = configMessage.configs.get("PACKAGES_MASTER_SNP_MORE_THAN_ZERO").data

            return False

        return True
    

    def validate_width(self,width):

        if width == None or width == "" :

            self.massage_error  = configMessage.configs.get("PACKAGES_MASTER_WIDTH_REQUIRED").data

            return False

        return True
    
    def validate_length(self,length):

        if length == None or length == "" :

            self.massage_error  = configMessage.configs.get("PACKAGES_MASTER_LENGTH_REQUIRED").data

            return False
        
        return True
    

    def validate_height(self,height):

        if height == None or height == "" :

            self.massage_error  = configMessage.configs.get("PACKAGES_MASTER_HEIGHT_REQUIRED").data

            return False
        
        return True
    
    def validate_weight(self,weight):

        if weight == None or weight == "" :

            self.massage_error  = configMessage.configs.get("PACKAGES_MASTER_WEIGHT_REQUIRED").data

            return False
        
        return True
    

    def create(self, package_obj):
      
        if not self.validate_station_code(package_obj['station_code']) :   
            
            return None
        
        elif not self.validate_package_code(package_obj['package_code']) :

            return None 
        
        elif not self.validate_package_no(package_obj['package_no']) :

            return None 
        
        elif  not self.validate_snp(package_obj['snp']) :

            return None
        
        elif not self.validate_width(package_obj['width']) :

            return None
        
        elif  not self.validate_length(package_obj['length']) :

            return None
        
        elif not self.validate_height(package_obj['height']) :

            return None
        
        elif not self.validate_weight(package_obj['weight']) :

            return None
        
        else : 

            package_list =  Package.objects.filter(package_no__iexact = package_obj['package_no'],is_active=False)

            if len(package_list) > 0 :

                package_list.update(
                    snp= package_obj['snp'],
                    width= package_obj['width'],
                    length= package_obj['length'],
                    height= package_obj['height'],
                    weight= package_obj['weight'],
                    image_url= package_obj['image_url'],
                    updated_by = package_obj['updated_by'],
                    updated_date = datetime.utcnow(),
                    is_active=True
                )

                return package_list[0]
                
            else : 
                    
                package = Package()
                package.package_code = package_obj['package_code']
                package.package_no = package_obj['package_no']
                package.snp = package_obj['snp']
                package.width = package_obj['width']
                package.length = package_obj['length']
                package.height = package_obj['height']
                package.weight = package_obj['weight']
                package.station_code = package_obj['station_code']
                package.image_url = package_obj['image_url']
                package.updated_by = package_obj['updated_by']
                package.updated_date = datetime.utcnow()
                package.is_active = True

                package.save()
                return package
    

    def update(self,package_obj):

        print(package_obj['package_no'])
        if  not self.validate_snp(package_obj['snp']) :

            return None
        
        elif not self.validate_width(package_obj['width']) :

            return None
        
        elif  not self.validate_length(package_obj['length']) :

            return None
        
        elif not self.validate_height(package_obj['height']) :

            return None
        
        elif not self.validate_weight(package_obj['weight']) :

            return None
        
        else : 

            package_list = Package.objects.filter(package_no__iexact = package_obj['package_no'])

            print(package_obj['image_url'])
            if len(package_list) > 0 :
                package_list.update(
                        package_code= package_obj['package_code'],
                        snp= package_obj['snp'],
                        width= package_obj['width'],
                        length= package_obj['length'],
                        height= package_obj['height'],
                        weight= package_obj['weight'],
                        station_code = package_obj['station_code'],
                        image_url = package_obj['image_url'],
                        updated_date = datetime.utcnow(),
                    )
                
                return package_list[0]

    @staticmethod
    def covert_data_list_to_serializer_list(package_list) :

        package_return_list = []

        for package_obj in package_list :

            package_Serializer = Package_Serializer()
            package_Serializer.station_code = package_obj[0]
            package_Serializer.package_code = package_obj[1]
            package_Serializer.package_no = package_obj[2]
            package_Serializer.snp = package_obj[3]
            package_Serializer.width = package_obj[4]
            package_Serializer.length = package_obj[5]
            package_Serializer.height = package_obj[6]
            package_Serializer.weight = package_obj[7]
            package_Serializer.image_url = package_obj[8]
            package_Serializer.updated_by = package_obj[9]
            package_Serializer.updated_date = package_obj[10]
           
            package_return_list.append(package_Serializer)
        
        return package_return_list
    
    @staticmethod
    def covert_data_list_to_CSV_list(package_list) :

        package_return_list = []

        for package_obj in package_list :

            package_return_list.append([
                package_obj[0],
                package_obj[1],
                package_obj[2],
                package_obj[3],
                package_obj[4],
                package_obj[5],
                package_obj[6],
                package_obj[7],
                "Yes" if package_obj[8] is not None and not package_obj[8] == "" else "No",
                package_obj[9],
                package_obj[10].strftime("%d/%m/%Y")
            ])
        
        return package_return_list

    

