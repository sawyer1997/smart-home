from datetime import datetime, timezone


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods

from .models import EnrolledDevice
from customer.models import ServiceLocation
from .utils import get_eusage_of_device
from .repository import get_query
from .forms import EnrolledDeviceForm


@require_http_methods(['GET'])
@login_required
def show_device_eusage(request, device_id):
    # start_date:  = request.POST.get('start_date')
    # end_date: str = request.POST.get('end_date')
    cumulative = False

    start_date = datetime(2022, 8, 3, 0, 0, 0, tzinfo=timezone.utc)
    end_date = datetime(2022, 8, 6, 23, 59, 59, tzinfo=timezone.utc)

    labels, values = get_eusage_of_device(device_id, start_date, end_date, cumulative)
    template_name = "customer/show_chart.html" if not cumulative else "customer/show_linechart.html"
    context = {
        'labels': labels,
        'values': values,
        'x_axis': 'Timestamp',
        'y_axis': 'EnergyUsage'
    }
    return render(request, template_name, context)


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

    return render(request, 'device/add_device.html', {'form': form, 'location': location})


@login_required
def delete_device(request, device_id):
    enrolled_device = get_object_or_404(EnrolledDevice, pk=device_id, location__user=request.user)
    if request.method == 'POST':
        enrolled_device.delete()
        messages.success(request, 'Device deleted successfully.')
        return redirect('customer:service_locations')
    return render(request, 'device/delete_device.html', {'enrolled_device': enrolled_device})


@login_required
def show_device_type_eusage(request):
    # start_date:  = request.POST.get('start_date')
    # end_date: str = request.POST.get('end_date')
    # cumulative = request.POST.get('cumulative')
    # device_type = request.POST.get('device_type')
    device_type = 'Bulb'
    start_date = datetime(2022, 8, 3, 0, 0, 0, tzinfo=timezone.utc)
    end_date = datetime(2022, 8, 6, 23, 59, 59, tzinfo=timezone.utc)
    cumulative = False
    sql_query = (
        f"SELECT "
        f"device_devicemodel.id AS devicemodelid, "
        f"device_enrolleddevice.id AS enrolleddeviceid, "
        f"device_devicemodel.model_name AS model_name, "
        f"device_devicemodel.device_type AS device_type "
        f"FROM device_devicemodel "
        f"INNER JOIN device_enrolleddevice "
        f"ON device_devicemodel.id = device_enrolleddevice.device_model_id "
        f"WHERE device_type = '{device_type}' "
    )
    enrolled_devices = get_query(sql_query)
    timestamps_dict = {}
    for enrolled_device in enrolled_devices:
        _, enrolled_device_id, _, _ = enrolled_device
        timestamps, energy_usages = get_eusage_of_device(enrolled_device_id, start_date, end_date)
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


@login_required
def show_service_location_eusage(request, service_location_id):
    cumulative = False
    start_date = datetime(2022, 8, 3, 0, 0, 0, tzinfo=timezone.utc)
    end_date = datetime(2022, 8, 6, 23, 59, 59, tzinfo=timezone.utc)
    enrolled_devices = EnrolledDevice.objects.raw(
        "SELECT * FROM devices_enrolleddevice "
        "WHERE location_id = %s ", [service_location_id]
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


@login_required
def show_user_eusage(request):
    cumulative = False
    start_date = datetime(2022, 8, 3, 0, 0, 0, tzinfo=timezone.utc)
    end_date = datetime(2022, 8, 6, 23, 59, 59, tzinfo=timezone.utc)
    user_id = request.user.id
    sql_query = (
        f"SELECT "
        f"ed.id AS enrolled_device_id, "
        f"ed.location_id as location_id , "
        f"FROM device_enrolleddevice ed "
        f"INNER JOIN customer_servicelocation sl "
        f"ON sl.id = ed.location_id "
        f"WHERE sl.user_id = {user_id}"
    )
    enrolled_devices = get_query(sql_query)
    timestamps_dict = {}
    for enrolled_device in enrolled_devices:
        enrolled_device_id, _ = enrolled_device
        timestamps, energy_usages = get_eusage_of_device(enrolled_device_id, start_date, end_date)
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
