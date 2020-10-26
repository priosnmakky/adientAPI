from rest_framework import serializers 
from customers.models import Customer
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
import datetime
from rest_framework.settings import api_settings


class CustomerSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    item = serializers.IntegerField()
    name = serializers.CharField(max_length=150)
    project = serializers.CharField(max_length=150)
    statio_code = serializers.CharField(max_length=150)
    description = serializers.CharField(max_length=350)
    customers_type = serializers.CharField(max_length=150)
    zone = serializers.CharField(max_length=150)
    province = serializers.CharField(max_length=150)
    address = serializers.CharField(max_length=350)
    lat = serializers.CharField(max_length=200,allow_blank=True)
    long = serializers.CharField(max_length=200,allow_blank=True)
    remark = serializers.CharField(max_length=250,allow_blank=True)


    def create(self, validated_data):
       
        return Customer.objects.create(**validated_data)