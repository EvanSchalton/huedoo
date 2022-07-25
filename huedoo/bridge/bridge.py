from typing import Any, Optional, TYPE_CHECKING
from uuid import UUID
import requests
from time import sleep
from http import HTTPStatus
from ipaddress import ip_address as _ip_address, IPv4Address, IPv6Address
from huedoo.config.config_handler_abc import ConfigHandlerABC
from huedoo.hue_api.models.resources import resource
from huedoo.hue_api.routes.device_settings import DeviceSetting

from ..hue_api import HueAPI, Resource, ResourceType

if TYPE_CHECKING:
    from huedoo.controls.light import Light


class Bridge:
    """
    Primary controller for interacting with the hue bridge
    """

    def __init__(self, config_handler: ConfigHandlerABC):
        self.api: Optional[HueAPI] = None
        self.config_handler = config_handler

        # self.ip_address: Optional[IPv4Address | IPv6Address] = None
        # if ip_address is not None:
        #     self.ip_address = _ip_address(ip_address)

        self.setup()

    @staticmethod
    def lookup_ip_address() -> IPv4Address | IPv6Address:
        """
        Connect to a bridge given it's IP Address
        or try to find it on the network
        """
        HUE_DISCOVERY_ENDPOINT = "https://discovery.meethue.com/"
        try:
            response = requests.get(HUE_DISCOVERY_ENDPOINT)
            attempt_count: int = 1
            while response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
                # print(f"Searching for Bridge [try {attempt_count}]")
                sleep(30)
                response = requests.get(HUE_DISCOVERY_ENDPOINT)
                attempt_count += 1

            bridges = response.json()
            ip_string = bridges[0]["internalipaddress"]
            # print(f"Bridge found at: {ip_string}")
            return _ip_address(ip_string)
        except Exception as error:
            # TODO: Custom Exception
            raise Exception("No Bridge Found") from error

    def setup(self):
        """
        Creates a HueAPI reference and connects to the bridge
        """
        self.api = HueAPI(
            bridge_ip=self.config_handler.data.ip_address
        )

    def register(self, app_name: str = "python-hue"):
        app_token = self.api.register_app(app_name)
        self.config_handler.write(
            app_name=app_name,
            app_token=app_token
        )

    @property
    def lights(self) -> list['Light']:
        from huedoo.controls.light import Light
        return [Light(resource=i, bridge=self) for i in self.api._list_resources() if i.type == ResourceType.LIGHT]

    def get_device(
        self,
        resource_type: ResourceType,
        id: Optional[str | UUID] = None,
        name: Optional[str] = None
    ) -> 'Light':
        from huedoo.controls.light import Light

        if isinstance(id, str):
            id = UUID(id)
        resource = self.api.get_device(
            resource_type=resource_type,
            id=id,
            name=name
        )

        if resource_type == ResourceType.LIGHT:
            return Light(
                resource=resource,
                bridge=self
            )

    def set_device(
        self,
        resource_type: ResourceType,
        id: Optional[str | UUID] = None,
        name: Optional[str] = None,
        device_settings: Optional[list[DeviceSetting]] = None,
        **kwargs
    ) -> Resource:
        # TODO: Should return an actual object
        if isinstance(id, str):
            id = UUID(id)

        params: dict[str, Any] = kwargs
        if device_settings is not None:
            for device_setting in device_settings:

                try:
                    # works with enums or dicts
                    device_setting = device_setting.value
                except AttributeError:
                    pass

                params.update(**device_setting)

        print("params:", params)
        return self.api.set_device(
            resource_type=resource_type,
            id=id,
            name=name,
            params=params
        )
