from http import HTTPStatus
from typing import Any, Optional
from uuid import UUID
from requests import Session, Request
from ipaddress import ip_address, IPv4Address, IPv6Address
from .models import (
    Route, HueAPIVersion,
    Resource, ResourceType,
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
        route: HueRoute | Route,
        data: Optional[dict[str, Any]] = None
    ):
        """
        Utility function for HTTP GET/PUT requests for the API
        """

        if isinstance(route, HueRoute):
            route = route.value

        DEFAULT_TIMEOUT_SECONDS = 10

        if self.session is None:
            self.setup_session()

        url = f"{self.get_uri(route.api_version)}{route.endpoint}"
        print("url:", url)
        request = Request(
            method=route.mode.value,
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
                verify=route.verify
            )
            # print("response:", response)

        except TimeoutError as error:
            # print(error)
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
        return token

    def _get_app_token(self, app_name: str = "python-hue") -> str:
        """
        Registers the app with the bridge and returns the token
        """
        if self.session is None:
            self.setup_session()
        # print("self.session", self.session)

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
        """
        List all devices on the bridge
        """
        resources = self.request(HueRoute.RESOURCES).json().get('data', [])
        return [Resource(**i) for i in resources]

    def _get_id_from_name(
        self,
        resource_type: ResourceType,
        name: str
    ) -> UUID:
        resources = self._list_resources()
        for resource in resources:
            try:
                if resource.metadata.name == name and resource.type == resource_type:
                    return resource.id
            except AttributeError:
                continue
        raise Exception(f"Cannot find device '{name}'")

    def _resolve_id(
        self,
        resource_type: ResourceType,
        id: Optional[UUID | str] = None,
        name: Optional[str] = None
    ) -> UUID:
        if id is None and name is None:
            raise Exception(f"Must provide an id or name")
        if id is not None and name is not None:
            raise Exception(f"Must provide either an id or name")

        if isinstance(id, str):
            id = UUID(id)
            return id

        if id is None and name is not None:
            id = self._get_id_from_name(resource_type, name)

        return id

    def get_device(
        self,
        resource_type: ResourceType,
        id: Optional[UUID | str] = None,
        name: Optional[str] = None
    ) -> Resource:
        """
        Lookup a device by it's id OR name
        """
        id = self._resolve_id(resource_type, id, name)

        route = HueRoute.GET_DEVICE.value
        if resource_type == ResourceType.LIGHT:
            route = HueRoute.GET_LIGHT.value

        if route.parameters is None:
            route.parameters = {}
        route.parameters['id'] = id

        response = self.request(route)
        # print(response.request.path_url)
        # print(response.request.headers)
        if response.status_code == HTTPStatus.NOT_FOUND:
            raise Exception(f"Cannot find device '{name}' [{id}]")

        device_json = response.json()['data'][0]
        # print(device_json)
        resource = Resource(**device_json)
        # print("resource:", resource)
        return resource

    def set_device(
        self,
        resource_type: ResourceType,
        params: dict[str, Any],
        id: Optional[UUID | str] = None,
        name: Optional[str] = None
    ):
        id = self._resolve_id(resource_type, id, name)

        route = HueRoute.PUT_DEVICE.value
        if resource_type == ResourceType.LIGHT:
            route = HueRoute.PUT_LIGHT.value

        if route.parameters is None:
            route.parameters = {}
        route.parameters['id'] = id

        response = self.request(route, data=params)

        print("response:", response)

        if response.status_code == HTTPStatus.NOT_FOUND:
            raise Exception(f"Cannot find device '{name}' [{id}]")

        return response
