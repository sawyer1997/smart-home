from .models import EnrolledDevice, ModelEvent, Notification
from .constants import EventType
from .repository import get_query


def get_eusage_of_device(device_id, start_date, end_date, cumulative=False):
    enrolled_device = EnrolledDevice.objects.raw(
        "SELECT * FROM device_enrolleddevice WHERE id = %s", [device_id]
    )[0]

    device_energy_event = ModelEvent.objects.raw(
        "SELECT * FROM device_modelevent where device_model_id = %s "
        "and event_type = %s", [enrolled_device.device_model.id, EventType.ENERGY_USAGE.value]
    )[0]

    labels = []
    values = []
    if start_date.date() == end_date.date():
        device_energy_notifications = Notification.objects.raw(
            "SELECT * FROM device_notification WHERE enrolled_device_id = %s "
            "AND model_event_id = %s "
            "AND time_stamp >= %s AND time_stamp <= %s ",
            [enrolled_device.id, device_energy_event.id,
             start_date.strftime('%Y-%m-%d %H:%M:%S'),
             end_date.strftime('%Y-%m-%d %H:%M:%S')]
        )
        if not cumulative:
            for notification in device_energy_notifications:
                labels.append(notification.time_stamp.strftime('%Y-%m-%d %H:%M:%S'))
                values.append(notification.event_value)
        else:
            last_value = 0
            for notification in device_energy_notifications:
                labels.append(notification.time_stamp.strftime('%Y-%m-%d %H:%M:%S'))
                last_value += notification.event_value
                values.append(last_value + notification.event_value)
    else:
        start_date_str = start_date.strftime('%Y-%m-%d %H:%M:%S')
        end_date_str = end_date.strftime('%Y-%m-%d %H:%M:%S')
        sql_query = (
            f"SELECT (time_stamp AT TIME ZONE 'UTC')::date as day, "
            f"SUM(event_value) as daily_sum "
            f"FROM device_notification "
            f"WHERE enrolled_device_id = {enrolled_device.id} AND "
            f"model_event_id = {device_energy_event.id} AND "
            f"time_stamp BETWEEN '{start_date_str}' AND '{end_date_str}' "
            f"GROUP BY (time_stamp AT TIME ZONE 'UTC')::date "
            f"ORDER BY (time_stamp AT TIME ZONE 'UTC')::date ASC "
        )
        daily_aggregation = get_query(sql_query)
        if not cumulative:
            for daily_value in daily_aggregation:
                labels.append(daily_value[0].strftime('%Y-%m-%d'))
                values.append(daily_value[1])
        else:
            last_value = 0
            for daily_value in daily_aggregation:
                labels.append(daily_value[0].strftime('%Y-%m-%d'))
                last_value += daily_value[1]
                values.append(last_value)
    return labels, values
