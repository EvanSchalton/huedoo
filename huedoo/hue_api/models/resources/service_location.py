from pydantic import BaseModel
from .resource_service import ResourceService
from .location import Location


class ServiceLocation(BaseModel):
    positions: list[Location]
    service: ResourceService
    position: Location
