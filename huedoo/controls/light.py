from typing import Optional
from uuid import UUID
from huedoo.hue_api.models import Resource, ResourceType
from huedoo import Bridge
from .base_classes import Dimmable


class Light(Dimmable):
    """
    A controller for a light
    """

    def __init__(
        self,
        bridge: Bridge,
        resource: Optional[Resource] = None,
        uuid: Optional[str | UUID] = None,
        name: Optional[str] = None
    ):

        super().__init__(
            resource=resource,
            bridge=bridge,
            uuid=uuid,
            name=name,
            resource_type=ResourceType.LIGHT
        )
