from enum import Enum


class DeviceType(Enum):
    Sensor = 1
    Actuator = 2
    Gateway = 3

    @classmethod
    def choices(cls):
        return [(key.value, key.name.replace('_', ' ')) for key in cls]
