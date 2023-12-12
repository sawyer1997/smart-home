from datetime import datetime, timezone

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Notification, ModelEvent, EnrolledDevice
from .constants import EventType


@require_http_methods(['GET'])
@login_required
def show_device_eusage(request, device_id):
    # start_date:  = request.POST.get('start_date')
    # end_date: str = request.POST.get('end_date')
    cumulative = False
    # TODO, query from the DB about the energy usage
    enrolled_device = EnrolledDevice.objects.get(id=device_id)
    device_energy_event = ModelEvent.objects.get(
        device_model=enrolled_device.device_model,
        event_type=EventType.ENERGY_USAGE.value,
    )
    start_date = datetime(2022, 8, 3, 0, 0, 0, tzinfo=timezone.utc)
    end_date = datetime(2022, 8, 3, 23, 59, 59, tzinfo=timezone.utc)
    device_energy_notifications = Notification.objects.filter(
        enrolled_device=enrolled_device,
        model_event=device_energy_event,
        time_stamp__gte=start_date,
        time_stamp__lte=end_date,
    )
    labels = []
    values = []
    if start_date == end_date:
        if not cumulative:
            for notification in device_energy_notifications:
                labels.append(notification.time_stamp)
                values.append(notification.event_value)
    else:
        pass
    context = {
        'labels': labels,
        'values': values,
        'x_axis': 'Timestamp',
        'y_axis': 'EnergyUsage'
    }
    print(f'{context = }')
    return render(request, "customer/show_chart.html", context)
