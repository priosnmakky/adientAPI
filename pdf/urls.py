#project/app/urls.py
from django.urls import path
from pdf import views
from django.conf.urls import url 
urlpatterns = [
    url(r'^api/render_pickup_pdf$',views.render_pickup_pdf),
    url(r'^api/render_truckplan_pdf$',views.render_truckplan_pdf)
]