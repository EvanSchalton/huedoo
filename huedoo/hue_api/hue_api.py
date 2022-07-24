from http import HTTPStatus
from typing import Any, Optional
from requests import Session, Request
from ipaddress import ip_address, IPv4Address, IPv6Address
from .models import (
    RequestMethod, Route, HueAPIVersion,
    Resource, ResourceType,
    AlertActionValue
)
import json
from .exceptions import BridgeButtonNotPushed, BridgePairingException, UnknownAppName
from .routes import HueRoute

# TODO: Implement logging


class HueAPI:
    """
    API for managine hue connections
    """

    session: Optional[Session] = None

    def __init__(
        self,
        bridge_ip: Optional[IPv4Address | IPv6Address | str] = None
    ):
        self.bridge_ip: Optional[IPv4Address | IPv6Address] = None
        if bridge_ip is not None:
            self.bridge_ip = ip_address(bridge_ip)

    def setup_session(self):
        """
        Setup the session w/ headers
        """
        self.session = Session()

    def request(
        self,
        route: HueRoute,
        data: Optional[dict[str, Any]] = None
    ):
        """ Utility function for HTTP GET/PUT requests for the API"""
        DEFAULT_TIMEOUT_SECONDS = 10

        if self.session is None:
            self.setup_session()

        url = f"{self.get_uri(route.value.api_version)}{route.value.endpoint}"
        request = Request(
            method=route.value.mode.value,
            url=url,
            data=json.dumps(data) if data is not None else None
        )

        # print("request:", request)

        prepared_request = self.session.prepare_request(request)
        # print("prepared_request:", prepared_request)

        try:
            response = self.session.send(
                prepared_request,
                timeout=DEFAULT_TIMEOUT_SECONDS,
                verify=route.value.verify
            )
            print("response:", response)

        except TimeoutError as error:
            print(error)
            # TODO: Custom Excpetion
            raise Exception("Timeout Error") from error

        return response

    def get_uri(self, api_version: HueAPIVersion) -> str:
        """
        Returns the API URI
        """
        if api_version == HueAPIVersion.V2:
            return f"https://{self.bridge_ip}/clip/v2"

        return f"https://{self.bridge_ip}"

    def register_app(self, app_name: str = "python-hue"):
        if self.session is None:
            self.setup_session()
        token = self._get_app_token(app_name)
        self.session.headers['hue-application-key'] = token

    def _get_app_token(self, app_name: str = "python-hue") -> str:
        """
        Registers the app with the bridge and returns the token
        """
        if self.session is None:
            self.setup_session()
        print("self.session", self.session)

        response = self.request(
            HueRoute.REGISTRATION,
            data={"devicetype": app_name},
        )

        if response.status_code == HTTPStatus.OK:
            response_json = response.json()

            for line in response_json:
                print(line)
                if 'success' in line:
                    print("line['success']", line['success'])
                    return line['success']
                if 'error' in line:
                    error_type = line['error']['type']
                    if error_type == 101:
                        raise BridgeButtonNotPushed()
                    if error_type == 7:
                        raise UnknownAppName(app_name)

                    raise BridgePairingException(line['error']['description'])

    def _list_resources(self) -> list[Resource]:
        resources = self.request(HueRoute.RESOURCES).json().get('data', [])
        return [Resource(**i) for i in resources]
