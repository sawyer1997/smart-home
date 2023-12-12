from enum import Enum


class EventType(Enum):
    DOOR = 'door'
    COOLING = 'cooling'
    TEMPERATURE = 'temperature'
    STATUS = 'status'
    BRIGHTNESS = 'brightness'
    WASH_MODE = 'wash_mode'
    ENERGY_USAGE = 'energy_usage'
