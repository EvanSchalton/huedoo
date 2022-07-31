from pydantic import BaseModel  # type:ignore
from .resource_service import ResourceService
from .location import Location


class ServiceLocation(BaseModel):
    positions: list[Location]
    service: ResourceService
    position: Location

    class Config:
        use_enum_values = False
