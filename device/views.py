from datetime import datetime, time

from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import EnrolledDevice
from customer.models import ServiceLocation
from .utils import get_eusage_of_device
from .repository import get_query
from .forms import EnrolledDeviceForm
from customer.forms import EnergyUsageForm


@login_required
def show_device_eusage(request, device_id):
    enrolled_device = EnrolledDevice.objects.get(id=device_id)
    if request.user != enrolled_device.location.user:
        messages.error(request, 'You do not have permission to view device energy usage!')
        return redirect(reverse('customer:detailed_service_locations',
                                kwargs={'location_id': enrolled_device.location.id}))
    if request.method == 'POST':
        device_eusage_form = EnergyUsageForm(request.POST)

        if not device_eusage_form.is_valid():
            messages.error(request, "Please enter valid data")
            return render(request, 'customer/show_stats.html',
                          {"eusage_form": EnergyUsageForm()})

        sl_eusage = device_eusage_form.cleaned_data
        cumulative = sl_eusage['cumulative']
        start_date = datetime.combine(sl_eusage['start_date'], time(0, 0, 0))
        end_date = datetime.combine(sl_eusage['end_date'], time(23, 59, 59))

        labels, values = get_eusage_of_device(device_id, start_date, end_date, cumulative)
        template_name = "customer/show_chart.html" if not cumulative else "customer/show_linechart.html"
        context = {
            'labels': labels,
            'values': values,
            'x_axis': 'Timestamp',
            'y_axis': 'EnergyUsage'
        }
        return render(request, template_name, context)

    device_eusage_form = EnergyUsageForm()
    return render(request, 'customer/show_stats.html', {
        'stats': 'Device Energy Stats',
        'eusage_form': device_eusage_form,
    })


@login_required
def add_device(request, location_id):
    location = get_object_or_404(ServiceLocation, pk=location_id, user=request.user)
    if request.method == 'POST':
        form = EnrolledDeviceForm(request.POST)
        if form.is_valid():
            enrolled_device = form.save(commit=False)
            enrolled_device.location = location
            enrolled_device.save()
            messages.success(request, 'Device added successfully.')
            return redirect('customer:service_locations')
    else:
        form = EnrolledDeviceForm()

    return render(request, 'device/enroll_device.html', {'form': form, 'location': location})


@login_required
def delete_device(request, device_id):
    enrolled_device = get_object_or_404(EnrolledDevice, pk=device_id, location__user=request.user)
    if request.method == 'POST':
        enrolled_device.is_active = False
        enrolled_device.save()
        messages.success(request, 'Device deleted successfully.')
        return redirect('customer:service_locations')
    return render(request, 'device/delete_device.html', {'enrolled_device': enrolled_device})


@login_required
def show_service_location_eusage(request, location_id):
    sl_instance = ServiceLocation.objects.raw(
        f"SELECT * from customer_servicelocation WHERE id = {location_id}"
    )
    if len(sl_instance) == 0:
        messages.error(request, "No location found!")
        return redirect(reverse('customer:service_locations'))
    sl_instance = sl_instance[0]
    if sl_instance.user != request.user:
        messages.error(request, 'You do not have permission to check this!')
        return redirect(reverse('customer:service_locations'))

    if request.method == 'POST':
        sl_eusage_form = EnergyUsageForm(request.POST)

        if not sl_eusage_form.is_valid():
            messages.error(request, "Please enter valid data")
            return render(request, 'customer/show_stats.html',
                          {"eusage_form": EnergyUsageForm()})

        sl_eusage = sl_eusage_form.cleaned_data
        cumulative = sl_eusage['cumulative']
        start_date = datetime.combine(sl_eusage['start_date'], time(0, 0, 0))
        end_date = datetime.combine(sl_eusage['end_date'], time(23, 59, 59))

        enrolled_devices = EnrolledDevice.objects.raw(
            "SELECT * FROM device_enrolleddevice "
            "WHERE location_id = %s ", [location_id]
        )
        timestamps_dict = {}
        for enrolled_device in enrolled_devices:
            timestamps, energy_usages = get_eusage_of_device(enrolled_device.id, start_date, end_date)
            for ind, timestamp in enumerate(timestamps):
                if timestamp not in timestamps_dict:
                    timestamps_dict[timestamp] = 0
                timestamps_dict[timestamp] += energy_usages[ind]
        context = {
            'labels': list(timestamps_dict.keys()),
            'values': list(timestamps_dict.values()),
            'x_axis': 'Timestamp',
            'y_axis': 'EnergyUsage'
        }
        template_name = "customer/show_chart.html" if not cumulative else "customer/show_linechart.html"
        return render(request, template_name, context)
    sl_eusage_form = EnergyUsageForm()
    return render(request, 'customer/show_stats.html', {
        'stats': 'Service Location Energy Stats',
        'eusage_form': sl_eusage_form
    })


@login_required
def show_user_eusage(request):
    if request.method == "POST":
        user_eusage_form = EnergyUsageForm(request.POST)

        if not user_eusage_form.is_valid():
            messages.error(request, "Please enter valid data")
            return render(request, 'customer/show_stats.html',
                          {"eusage_form": EnergyUsageForm()})

        user_eusage = user_eusage_form.cleaned_data
        cumulative = user_eusage['cumulative']
        start_date = datetime.combine(user_eusage['start_date'], time(0, 0, 0))
        end_date = datetime.combine(user_eusage['end_date'], time(23, 59, 59))
        user_id = request.user.id
        sql_query = (
            f"SELECT "
            f"ed.id AS enrolled_device_id, "
            f"ed.location_id AS location_id "
            f"FROM device_enrolleddevice AS ed "
            f"INNER JOIN customer_servicelocation AS sl "
            f"ON sl.id = ed.location_id "
            f"WHERE sl.user_id = {user_id}"
        )
        enrolled_devices = get_query(sql_query)
        timestamps_dict = {}
        for enrolled_device in enrolled_devices:
            enrolled_device_id, _ = enrolled_device
            timestamps, energy_usages = get_eusage_of_device(enrolled_device_id, start_date, end_date, cumulative)
            for ind, timestamp in enumerate(timestamps):
                if timestamp not in timestamps_dict:
                    timestamps_dict[timestamp] = 0
                timestamps_dict[timestamp] += energy_usages[ind]
        context = {
            'labels': list(timestamps_dict.keys()),
            'values': list(timestamps_dict.values()),
            'x_axis': 'Timestamp',
            'y_axis': 'EnergyUsage'
        }
        template_name = "customer/show_chart.html" if not cumulative else "customer/show_linechart.html"
        return render(request, template_name, context)

    user_eusage_form = EnergyUsageForm()
    return render(request, 'customer/show_stats.html', {
        'stats': 'User Energy Stats',
        'eusage_form': user_eusage_form
    })


@login_required
def get_devices(request, location_id):
    sl_instance = ServiceLocation.objects.raw(
        f"SELECT * from customer_servicelocation WHERE id = {location_id}"
    )
    if len(sl_instance) == 0:
        messages.error(request, "No location found!")
        return redirect(reverse('customer:service_locations'))
    sl_instance = sl_instance[0]
    if sl_instance.user != request.user:
        messages.error(request, 'You do not have permission to check this!')
        return redirect(reverse('customer:service_locations'))
    enrolled_devices = EnrolledDevice.objects.raw(
        f"SELECT * from device_enrolleddevice WHERE location_id = {location_id} AND is_active = 't'"
    )
    enrolled_devices = list(enrolled_devices)
    return render(request, 'device/list_enrolled_device.html',
                  {'enrolled_devices': enrolled_devices,
                   'location_id': location_id}
                  )
