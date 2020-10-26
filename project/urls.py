from django.conf.urls import url 
from project import views 
 
urlpatterns = [ 
    url(r'^api/projects$', views.project_list),
]
