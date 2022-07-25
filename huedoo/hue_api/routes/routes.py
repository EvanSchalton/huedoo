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
    GET_DEVICE = Route(
        path="/resource/device/$id",
        verify=False,
    )
    PUT_DEVICE = Route(
        mode=RequestMethod.PUT,
        path="/resource/device/$id",
        verify=False,
    )
    GET_LIGHT = Route(
        path="/resource/light/$id",
        verify=False,
    )
    PUT_LIGHT = Route(
        mode=RequestMethod.PUT,
        path="/resource/light/$id",
        verify=False,
    )
