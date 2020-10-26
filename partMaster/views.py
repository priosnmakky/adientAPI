from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from partMaster.models import Part_master
from model_DTO.validateError import validateError
from partMaster.serializers import Part_masterSerializer
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated


@api_view(['GET', 'POST', 'DELETE'])
def part_master_list(request):
    # if request.method == 'GET':
    #     tutorials = Tutorial.objects.all()
        
    #     title = request.GET.get('title', None)
    #     if title is not None:
    #         tutorials = tutorials.filter(title__icontains=title)
        
    #     tutorials_serializer = TutorialSerializer(tutorials, many=True)
    #     return JsonResponse(tutorials_serializer.data, safe=False)
    #     # 'safe=False' for objects serialization
    if request.method == 'GET':
        part_master_list = Part_master.objects.all()
        
        # title = request.GET.get('title', None)
        # if title is not None:
        #     tutorials = tutorials.filter(title__icontains=title)
        
        part_master_serializer = Part_masterSerializer(part_master_list, many=True)
        return JsonResponse(part_master_serializer.data, safe=False)

 
    elif request.method == 'POST':
        part_master_data = JSONParser().parse(request)
        part_master_serializer = Part_masterSerializer(data=part_master_data)
        if part_master_serializer.is_valid():
            part_master_serializer.save()
            return JsonResponse(part_master_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(part_master_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 