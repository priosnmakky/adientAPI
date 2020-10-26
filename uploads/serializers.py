from rest_framework import serializers
from uploads.models import File
from model_DTO.validateError import validateError





# class StopOncomingSerialier(serializers.Serializer):
#     idn = serializers.IntegerField(read_only=True)
#     buses = BusSerializer(many=True)

class FileSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    file_no = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    file_name = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    file_size = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    order_count = serializers.IntegerField(allow_null=True,required=False)
    status = serializers.BooleanField(allow_null=True,required=False)
    customer_id = serializers.CharField(max_length=15,allow_blank=True,allow_null=True,required=False)
    project_id = serializers.CharField(max_length=15,allow_blank=True,allow_null=True,required=False)
    created_by = serializers.CharField(max_length=15,allow_blank=True,allow_null=True,required=False)
    created_date = serializers.DateTimeField(format="%d-%m-%Y ", input_formats=['%d-%m-%Y',],allow_null=True,required=False)
    updated_by = serializers.CharField(allow_blank=True,allow_null=True,required=False)
    updated_date = serializers.DateTimeField(format="%d-%m-%Y", input_formats=['%d-%m-%Y',],allow_null=True,required=False)
    file = serializers.FileField()


    class Meta:     #instead of meta write Meta (Capital M)
        model = File
        fields = '__all__'
 

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return File.objects.create(**validated_data)


class validateErrorSerializer(serializers.Serializer):

    error = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    row = serializers.IntegerField(allow_null=True,required=False)
    column = serializers.IntegerField(allow_null=True,required=False)
    status = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)


class validateErrorSerializerList(serializers.Serializer):

    status = serializers.CharField(max_length=150,allow_blank=True,allow_null=True,required=False)
    validateErrorList = validateErrorSerializer(many=True)
    fileList  = FileSerializer(many=True)