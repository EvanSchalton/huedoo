from huedoo.hue_api.routes.device_settings import DeviceSetting
from typing import Optional
from uuid import UUID
from huedoo import Bridge
from ...hue_api.models import Resource, ResourceType


class Device:
    """
    A Philips Hue Device
    """

    def __init__(
        self,
        bridge: Bridge,
        resource: Optional[Resource] = None,
        uuid: Optional[UUID] = None,
        name: Optional[str] = None,
        resource_type: Optional[ResourceType] = None
    ):

        # TODO: if Resource isn't provided ResourceType must be
        self.bridge = bridge
        self.resource_type = resource_type

        if resource is not None:
            self.resource = resource
        else:
            self.resource = self.bridge.api.get_device(
                resource_type=resource_type,
                uuid=uuid,
                name=name
            )
        if resource_type is None:
            resource_type = self.resource.type

        if name is None:
            name = self.resource.metadata.name

        if uuid is None:
            uuid = self.resource.id

        self.resource_type = resource_type
        self.name = name
        self.uuid = uuid

    def set(
        self,
        device_settings: Optional[list[DeviceSetting]] = None,
        **kwargs
    ):
        """
        Set the device properties
        """

        self.bridge.set_device(
            resource_type=self.resource.type,
            uuid=self.uuid,
            device_settings=device_settings,
            **kwargs
        )

    def refresh(self, updated_resource: Optional[Resource] = None):
        """
        Refresh the latest status of the device
        """
        if updated_resource is not None:
            self.resource = updated_resource
            return

        self.resource = self.bridge.api.get_device(
            resource_type=self.resource_type,
            uuid=self.uuid
        )
