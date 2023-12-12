from django.urls import path
from . import views

urlpatterns = [
    path('<int:device_id>/show_device_eusage/', views.show_device_eusage, name='show_device_eusage'),
]
