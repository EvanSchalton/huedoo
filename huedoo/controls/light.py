from typing import Optional
from uuid import UUID
from huedoo.hue_api.models import Resource
from huedoo import Bridge
from huedoo.hue_api.models.resources.resource_type import ResourceType
from .base_classes import Dimmable


class Light(Dimmable):
    """
    A controller for a light
    """

    def __init__(
        self,
        bridge: Bridge,
        resource: Optional[Resource] = None,
        id: Optional[str | UUID] = None,
        name: Optional[str] = None
    ):
        self.bridge = bridge

        if resource is not None:
            self.resource = resource
        else:
            self.resource = self.bridge.api.get_device(
                resource_type=ResourceType.LIGHT,
                id=id,
                name=name
            )

        super().__init__(
            resource=self.resource,
            bridge=self.bridge
        )
