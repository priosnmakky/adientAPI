from django.conf.urls import url 
from customers import views 
 
urlpatterns = [ 
    url(r'^api/customers$', views.customer_list),
]
