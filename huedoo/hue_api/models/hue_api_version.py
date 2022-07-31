from ...utilities import Enum


class HueAPIVersion(Enum):
    """
    Allows for Endpoint selection based on Hue API Version
    """
    V1 = 1
    V2 = 2
