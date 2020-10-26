from django.conf.urls import url 
from .views import *
from django.urls import path
 
urlpatterns = [ 
    path('api/upload', FileUploadView.as_view()),
    path('api/files', get),
    path('api/get_files', file_list),
    path('api/get_order', order_list),
    path('api/comfirm', confirm),
    path('api/not_comfirm', not_confirm),
    path('api/search_miss_match', search_miss_match),
    path('api/search_pending_order', search_pending_order),
    path('api/search_upload_order_log_file', search_upload_order_log_file),
    path('api/search_order_transaction', search_order_transaction),
    path('api/match_order', match_order)
]
