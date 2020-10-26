from rest_framework import serializers 
from partMaster.models import Part_master
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
import datetime
from rest_framework.settings import api_settings


class Part_masterSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    item_on = serializers.IntegerField()
    part_number = serializers.CharField(max_length=150)
    part_name = serializers.CharField(max_length=150)
    supplier_code = serializers.CharField(max_length=150)
    project_code = serializers.CharField(max_length=150)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Part_master.objects.create(**validated_data)
 
