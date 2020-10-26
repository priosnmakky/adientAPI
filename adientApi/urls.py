from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url, include 
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()
urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path("api/accounts/",include("accounts.urls")),
    path("api/events/",include("events.urls")),

    
    url(r'^', include('project.urls')),
    url(r'^', include('customers.urls')),
    url(r'^', include('uploads.urls')),
    url(r'^', include('partMaster.urls')),
    url(r'^', include('order.urls')),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,}),

    url(r'^',include("master_data.urls")),
    url(r'^',include("truck_plan_management.urls")),
    url(r'^',include('pdf.urls')),
    path('pdf/', include('pdf.urls'), name='pdf'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

