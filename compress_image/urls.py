from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib import admin
from mainApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.send_auto_bulk_whatsapp_message, name='send_auto_bulk_whatsapp_message'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
