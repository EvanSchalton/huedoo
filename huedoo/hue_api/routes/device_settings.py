from ...utilities import Enum
from .device_setting_functions import *


class DeviceSetting(Enum):
    TURN_ON = {'on': {'on': True}}
    TURN_OFF = {'on': {'on': False}}
    BRIGHTNESS = set_brightness
