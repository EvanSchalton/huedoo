from typing import Optional
from huedoo import Bridge
from huedoo.hue_api.routes.device_settings import DeviceSetting
from ...hue_api.models import Resource, ResourceType
from .device import Device
from uuid import UUID


class Switchable(Device):
    """
    Turn something on and off
    """

    def __init__(
        self,
        bridge: Bridge,
        resource: Optional[Resource] = None,
        uuid: Optional[UUID] = None,
        name: Optional[str] = None,
        resource_type: Optional[ResourceType] = None
    ):
        super().__init__(
            bridge=bridge,
            resource=resource,
            uuid=uuid,
            name=name,
            resource_type=resource_type
        )

    def turn_on(self, *args: list[DeviceSetting], **kwargs):
        """
        Turn on switchable
        """
        self.set(
            device_settings=[
                DeviceSetting.TURN_ON,
                *args
            ],
            **kwargs
        )
        self.refresh()

    def turn_off(self, *args: list[DeviceSetting], **kwargs):
        """
        Turn off switchable
        """
        self.set(
            device_settings=[
                DeviceSetting.TURN_OFF,
                *args
            ],
            **kwargs
        )
        self.refresh()

    def toggle(self, **kwargs):
        """
        Turn off/on switchable
        """
        if self.is_on:
            self.turn_off(**kwargs)
            return
        self.turn_on(**kwargs)

    @property
    def is_on(self) -> bool:
        """
        Return the on/off status of the switchable
        """
        self.refresh()
        return self.resource.on.on
