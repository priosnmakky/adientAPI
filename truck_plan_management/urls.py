from django.conf.urls import url 
from .views import *

urlpatterns = [
    url(r'^api/truck_plan_management/search_order_for_generate_pickup$',search_order_for_generate_pickup),
    url(r'^api/truck_plan_management/search_generate_truck_plan$',search_generate_truck_plan),
    url(r'^api/truck_plan_management/generate_PUS$',generate_PUS),
    url(r'^api/truck_plan_management/generate_truck_plan$',generate_truck_plan),
    url(r'^api/truck_plan_management/create_route$',create_route),
    url(r'^api/truck_plan_management/search_and_print_PUS$',search_and_print_PUS),
    url(r'^api/truck_plan_management/search_and_print_truck_plan$',search_and_print_truck_plan),
    url(r'^api/truck_plan_management/get_order_by_pickup_no$',get_order_by_pickup_no),
    url(r'^api/truck_plan_management/get_pickup_by_truckPlan_no$',get_pickup_by_truckPlan_no),
    url(r'^api/truck_plan_management/deleted_order_in_pickup$',deleted_order_in_pickup),
    url(r'^api/truck_plan_management/deleted_pickup_in_truckplan$',deleted_pickup_in_truckplan),
    url(r'^api/truck_plan_management/add_order_in_pickup$',add_order_in_pickup),
    url(r'^api/truck_plan_management/add_pickup_in_truckplan$',add_pickup_in_truckplan),
    url(r'^api/truck_plan_management/delete_pickUp$',delete_pickUp),
    url(r'^api/truck_plan_management/delete_truckplan$',delete_truckplan)
]
