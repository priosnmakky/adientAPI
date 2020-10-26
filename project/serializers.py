from rest_framework import serializers 
from project.models import Project
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
import datetime
from rest_framework.settings import api_settings


class ProjectSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    item = serializers.IntegerField()
    customer_code = serializers.CharField(max_length=150)
    customer_description = serializers.CharField(max_length=250)
    project_code = serializers.CharField(max_length=250)
    transporter = serializers.CharField(max_length=250)
    effective_date = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", input_formats=['%d-%m-%Y %H:%M:%S',])
    expire_date = serializers.DateTimeField()

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Project.objects.create(**validated_data)
 
    # class Meta:
    #     model = Project
    #     effective_date = serializers.DateField(format="%d-%m-%Y", input_formats=['%d-%m-%Y',])


    #     fields = ('item',
    #               'customer_code',
    #               'customer_description',
    #               'project_code',
    #               'transporter',
    #               'effective_date',
    #               'expire_date')
                  
    #     def to_representation(self, instance):
    #         representation = super(ProjectSerializer, self).to_representation(instance)
    #         representation['effective_date'] = 'lllllll'
    #         return {
    #             "id": "sdsfsdf",
            # }
