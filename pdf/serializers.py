from rest_framework import serializers 

class PDF_Serializer_DTO(serializers.Serializer):

    serviceStatus = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    massage = serializers.CharField(max_length=50,allow_blank=True,allow_null=True,required=False)
    pdf_name = serializers.CharField(max_length=300,allow_blank=True,allow_null=True,required=False)
