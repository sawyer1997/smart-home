from django.urls import path
from . import views

app_name = "device"
urlpatterns = [
    path('<int:device_id>/show_device_eusage/', views.show_device_eusage, name='show_device_eusage'),
    path('add_device/<int:location_id>/', views.add_device, name='add_device'),
    path('delete_device/<int:device_id>/', views.delete_device, name='delete_device'),
]
