from typing import Optional
import requests
from time import sleep
from http import HTTPStatus
from ipaddress import ip_address as _ip_address, IPv4Address, IPv6Address
from huedoo.config.config_handler_abc import ConfigHandlerABC

from huedoo.hue_api.hue_api import HueAPI, HueAPIVersion


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
