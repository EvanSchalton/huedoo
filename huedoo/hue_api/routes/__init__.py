from enum import Enum
from ..models import Route, RequestMethod, HueAPIVersion


class HueRoute(Enum):
    """
    Hue Route Deffinitions
    """
    REGISTRATION = Route(
        mode=RequestMethod.POST,
        api_version=HueAPIVersion.V1,
        verify=False
    )
    RESOURCES = Route(
        path="/resource",
        verify=False
    )
