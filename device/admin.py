from django.contrib import admin
from .models import DeviceModel, EnrolledDevice, EnergyPrice, ModelEvent, Notification

# Register your models here.
admin.site.register(DeviceModel)
admin.site.register(EnrolledDevice)
admin.site.register(EnergyPrice)
admin.site.register(ModelEvent)
admin.site.register(Notification)
