from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator
from datetime import datetime, timedelta, timezone
import random

from customer.models import ServiceLocation


class DeviceModel(models.Model):

    model_name = models.CharField(
        max_length=20,
        verbose_name='ModelName',
        null=False,
    )
    device_type = models.CharField(
        max_length=30,
        verbose_name='DeviceType',
        null=False,
    )

    def __str__(self):
        return f'{self.model_name}_{self.device_type}_{self.id}'


class EnrolledDevice(models.Model):

    location = models.ForeignKey(ServiceLocation, on_delete=models.CASCADE)
    device_model = models.ForeignKey(DeviceModel, on_delete=models.CASCADE)

    def __str__(self):
        return f'{str(self.location)}_{str(self.device_model)}'


class EnergyPrice(models.Model):

    zipcode = models.CharField(
        default='00000',
        verbose_name='ZipCode',
        help_text='Enter the zipcode',
        validators=[MinLengthValidator(5)],
        null=False,
    )
    time_stamp = models.DateTimeField(
        verbose_name='TimeStamp',
        null=False,
    )
    price_per_unit = models.FloatField(
        null=False,
        verbose_name='PricePerUnit',
        validators=[MinValueValidator(0.1)],
    )

    @classmethod
    def make_entries(cls):
        zipcodes = ['11213', '08619']
        for zipcode in zipcodes:
            start_timestamp = datetime(2022, 8, 1, 0, 0, 0, tzinfo=timezone.utc)
            end_timestamp = datetime(2022, 10, 1, 12, 0, 0, tzinfo=timezone.utc)
            while start_timestamp < end_timestamp:
                new_entry = EnergyPrice()
                new_entry.zipcode = zipcode
                new_entry.price_per_unit = random.randint(1, 10)
                new_entry.time_stamp = start_timestamp
                print(f'{zipcode = } {new_entry.price_per_unit = } {start_timestamp.strftime("%Y-%m-%d %H:%M")}')
                new_entry.save()
                start_timestamp += timedelta(hours=1)
        return


class ModelEvent(models.Model):

    device_model = models.ForeignKey(DeviceModel, on_delete=models.CASCADE)
    event_type = models.CharField(
        max_length=50,
        null=False,
    )
    default_event_value = models.IntegerField(
        null=False,
    )

    def __str__(self):
        return f'{str(self.device_model)}_{self.event_type}_{self.default_event_value}_{self.id}'


class Notification(models.Model):

    enrolled_device = models.ForeignKey(EnrolledDevice, on_delete=models.CASCADE)
    model_event = models.ForeignKey(ModelEvent, on_delete=models.CASCADE)
    event_value = models.IntegerField(
        null=False,
    )
    time_stamp = models.DateTimeField(
        verbose_name='TimeStamp',
        null=False,
    )

    @staticmethod
    def make_entries_for_bulb():
        bulb1 = EnrolledDevice.objects.get(id=3)
        bulb2 = EnrolledDevice.objects.get(id=4)
        energy_event = ModelEvent.objects.get(id=8)
        start_timestamp = datetime(2022, 8, 1, 8, 0, 0, tzinfo=timezone.utc)
        end_timestamp = datetime(2022, 10, 1, 8, 0, 0, tzinfo=timezone.utc)
        while start_timestamp < end_timestamp:
            new_entry = Notification()
            new_entry.event_value = random.randint(10, 20)
            new_entry.time_stamp = start_timestamp
            new_entry.model_event = energy_event
            new_entry.enrolled_device = bulb1 if 8 <= start_timestamp.hour <= 10 else bulb2
            new_entry.save()
            start_timestamp += timedelta(hours=1)
        return

    @classmethod
    def make_entries_for_fridge(cls):
        start_timestamp = datetime(2022, 8, 1, 0, 0, 0, tzinfo=timezone.utc)
        end_timestamp = datetime(2022, 10, 1, 0, 0, 0, tzinfo=timezone.utc)
        energy_event = ModelEvent.objects.get(id=5)
        fridge = EnrolledDevice.objects.get(id=1)
        while start_timestamp < end_timestamp:
            new_entry = Notification()
            new_entry.event_value = random.randint(100, 300)
            new_entry.time_stamp = start_timestamp
            new_entry.model_event = energy_event
            new_entry.enrolled_device = fridge
            new_entry.save()
            start_timestamp += timedelta(hours=1)
        return

    @classmethod
    def make_entries_for_washer(cls):
        start_timestamp = datetime(2022, 8, 1, 8, 0, 0, tzinfo=timezone.utc)
        end_timestamp = datetime(2022, 10, 1, 8, 0, 0, tzinfo=timezone.utc)
        energy_event = ModelEvent.objects.get(id=11)
        washer = EnrolledDevice.objects.get(id=2)
        while start_timestamp < end_timestamp:
            new_entry = Notification()
            new_entry.event_value = random.randint(300, 500)
            new_entry.time_stamp = start_timestamp
            new_entry.model_event = energy_event
            new_entry.enrolled_device = washer
            new_entry.save()
            start_timestamp += timedelta(days=1)
        return
