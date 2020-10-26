from django.conf.urls import url 
from master_data import views 
 
urlpatterns = [ 
    url(r'^api/master/part$', views.part_list),
    url(r'^api/master/router$', views.router_list),
    url(r'^api/master/project$', views.project_list),
    url(r'^api/master/upload_route_master$',views.upload_route_master),
    url(r'^api/master/seach_project$', views.seach_project),
    url(r'^api/master/seach_customer$', views.seach_customer),
    url(r'^api/master/seach_part$', views.seach_part),
    url(r'^api/master/seach_package$', views.seach_package),
    url(r'^api/master/seach_truck$', views.seach_truck),
    url(r'^api/master/seach_driver$', views.seach_driver),
    url(r'^api/master/search_route_master', views.search_route_master),
    url(r'^api/master/search_route_info', views.search_route_info),
    url(r'^api/master/search_calendarMaster', views.search_calendarMaster),
    url(r'^api/master/comfirm_part$', views.comfirm_part),
    url(r'^api/master/deleted_customer$', views.deleted_customer),
    url(r'^api/master/deleted_project$', views.deleted_project),
    url(r'^api/master/deleted_part$', views.deleted_part),
    url(r'^api/master/deleted_package$', views.deleted_package),
    url(r'^api/master/deleted_truck$', views.deleted_truck),
    url(r'^api/master/deleted_driver$', views.deleted_driver),
    url(r'^api/master/deleted_routeInfo$', views.deleted_routeInfo),
    url(r'^api/master/deleted_calendarMaster$', views.deleted_calendarMaster),
    url(r'^api/master/deleted_routeMaster$', views.deleted_routeMaster),
    url(r'^api/master/edited_project$', views.edited_project),
    url(r'^api/master/edited_part$', views.edited_part),
    url(r'^api/master/edited_customer$', views.edited_customer),
    url(r'^api/master/edited_package$', views.edited_package),
    url(r'^api/master/edited_truck$', views.edited_truck),
    url(r'^api/master/edited_driver$', views.edited_driver),
    url(r'^api/master/edited_routeInfo$',views.edited_routeInfo),
    url(r'^api/master/edited_calendarMaster$',views.edited_calendarMaster),
    url(r'^api/master/customer$', views.customer_list),
    url(r'^api/master/package$', views.package_list),
    url(r'^api/master/supplier$', views.supplier_list),
    url(r'^api/master/plant$', views.plant_list),
    url(r'^api/master/truck$', views.truck_list),
    url(r'^api/master/driver$', views.driver_list),
    url(r'^api/master/routeInfo$', views.routeInfo_list),
    url(r'^api/master/calendarMaster$', views.calendarMaster_list),
    url(r'^api/master/routeMaster$', views.routeMaster_list),
    url(r'^api/master/add_part_master$', views.add_part_master),
    url(r'^api/master/add_packages_master$', views.add_packages_master)

]