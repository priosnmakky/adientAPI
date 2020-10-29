from model_DTO.base_DTO import base_DTO

class SerializerMapping:

    base_obj = base_DTO()

    def mapping_list_successful(self,serialiser,serialiser_list,massage,csv_name):

        self.base_obj.serviceStatus = "success"
        self.base_obj.massage = massage
        self.base_obj.data_list = serialiser
        self.base_obj.csv_name = csv_name

        serialiser_list = serialiser_list(self.base_obj)

        return serialiser_list
    
    def mapping_obj_successful(self,serialiser,serialiser_DTO,massage,csv_name):

        self.base_obj.serviceStatus = "success"
        self.base_obj.massage = massage
        self.base_obj.data = serialiser
        self.base_obj.csv_name = csv_name

        serialiser_DTO = serialiser_DTO(self.base_obj)

        return serialiser_DTO
    
    def mapping_list_error (self,serialiser_list,massage):

        self.base_obj.serviceStatus = "Error"
        self.base_obj.massage = massage
        self.base_obj.data_list = None
        self.base_obj.csv_name = None

        serialiser_list = serialiser_list(self.base_obj)

        return serialiser_list
    
    def mapping_obj_error (self,serialiser_DTO,massage):

        self.base_obj.serviceStatus = "Error"
        self.base_obj.massage = massage
        self.base_obj.data_list = None
        self.base_obj.csv_name = None

        serialiser_DTO = serialiser_DTO(self.base_obj)

        return serialiser_DTO

    def mapping_pdf (self,serialiser_DTO,serviceStatus,massage,pdf_name):

        self.base_obj.serviceStatus = serviceStatus
        self.base_obj.massage = massage
        self.base_obj.pdf_name = pdf_name

        serialiser_DTO = serialiser_DTO(self.base_obj)

        return serialiser_DTO
    
    @staticmethod
    def mapping_serializer_obj (self,serialiser_DTO,data,serviceStatus,massage,csv_name,pdf_name,validate_error_list):

        self.base_obj.data = data
        self.base_obj.serviceStatus = serviceStatus
        self.base_obj.massage = massage
        self.base_obj.csv_name = csv_name
        self.base_obj.pdf_name = pdf_name
        self.base_obj.validate_error_list = validate_error_list

        serialiser_DTO = serialiser_DTO(self.base_obj)

        return serialiser_DTO
    
 
    def mapping_serializer_list (self,serialiser_DTO,data_list,serviceStatus,massage,csv_name,pdf_name,validate_error_list):

        self.base_obj.data_list = data_list
        self.base_obj.serviceStatus = serviceStatus
        self.base_obj.massage = massage
        self.base_obj.csv_name = csv_name
        self.base_obj.pdf_name = pdf_name
        self.base_obj.validate_error_list = validate_error_list

        serialiser_DTO = serialiser_DTO(self.base_obj)

        return serialiser_DTO
    


      