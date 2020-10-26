from django.conf.urls import url 
from partMaster import views 
 
urlpatterns = [ 
    url(r'^api/part_master$', views.part_master_list),
]
