from typing import Optional
from huedoo import Bridge
from huedoo.hue_api.routes.device_settings import DeviceSetting
from ...hue_api.models import Resource


class Switchable:
    """
    Turn something on and off
    """

    def __init__(
        self,
        resource: Resource,
        bridge: Bridge
    ):
        self.resource = resource
        self.bridge = bridge

    def turn_on(self, *args: list[DeviceSetting], **kwargs):
        """
        Turn on switchable
        """
        self.bridge.set_device(
            resource_type=self.resource.type,
            id=self.resource.id,
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
        self.bridge.set_device(
            resource_type=self.resource.type,
            id=self.resource.id,
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

    def refresh(self, updated_resource: Optional[Resource] = None):
        """
        Refresh the latest status of the switchable
        """
        print("refreshing")
        if updated_resource:
            self.resource = updated_resource
            return

        self.resource = self.bridge.api.get_device(
            resource_type=self.resource.type,
            id=self.resource.id
        )

    @property
    def is_on(self) -> bool:
        """
        Return the on/off status of the switchable
        """
        self.refresh()
        return self.resource.on.on
