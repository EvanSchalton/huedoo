from typing import Optional
from pydantic import BaseModel
from .resource_service import ResourceService
from .resource_configuration_where import ResourceConfigurationWhere
from .resource_configuration_what import ResourceConfigurationWhat
from .resource_configuration_when_constrained import ResourceConfigurationWhenConstrained


class ResourceConfiguration(BaseModel):
    end_scene: Optional[ResourceService] = None
    end_state: Optional[str] = None  # TODO: Enum
    what: Optional[list[ResourceConfigurationWhat]] = None
    where: list[ResourceConfigurationWhere]
    when_constrained: Optional[ResourceConfigurationWhenConstrained] = None
