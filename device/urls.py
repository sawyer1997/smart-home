from django.urls import path
from . import views

app_name = "device"
urlpatterns = [
    path('<int:device_id>/show_device_eusage/', views.show_device_eusage, name='show_device_eusage'),

    path('add_device/<int:location_id>/', views.add_device, name='add_device'),

    path('delete_device/<int:device_id>/', views.delete_device, name='delete_device'),

    path('show_user_eusage/', views.show_user_eusage, name='show_user_eusage'),

    path('show_sl_eusage/<int:location_id>/', views.show_service_location_eusage, name='show_sl_eusage'),

    path('get_devices/<int:location_id>/', views.get_devices, name='get_devices'),
]
