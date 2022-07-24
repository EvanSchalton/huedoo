from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from .resource_type import ResourceType
from .resource_service import ResourceService
from .resource_metadata import ResourceMetadata
from .resource_product_data import ResourceProductData

from .resource_alert import ResourceAlert
from .resource_color import ResourceColor
from .resource_color_temperature import ResourceColorTemperature
from .resource_dimming import ResourceDimming
from .resource_dynamics import ResourceDynamics
from .resource_effects import ResourceEffects
from .resource_configuration import ResourceConfiguration
from .schema_ref import SchemaRef
from .resource_button import ResourceButton
from .resource_configuration_depends import ResourceConfigurationDepends
from .resource_location import ResourceLocation
from .resource_channel import ResourceChannel
from .resource_stream_proxy import ResourceStreamProxy
from .resource_motion import ResourceMotion
from .resource_on import ResourceOn
from .resource_light import ResourceLight
from .resource_power_state import ResourcePowerState
from .resource_time_zone import ResourceTimeZone
from .resource_segments import ResourceSegments


class Resource(BaseModel):
    alert: Optional[ResourceAlert] = None
    color: Optional[ResourceColor]
    color_temperature: Optional[ResourceColorTemperature] = None
    color_temperature_delta: Optional[dict[str, str]] = None
    dimming: Optional[ResourceDimming] = None
    dimming_delta: Optional[dict[str, str]] = None
    dynamics: Optional[ResourceDynamics] = None
    effects: Optional[ResourceEffects] = None
    children: Optional[list[ResourceService]] = None
    configuration_type: Optional[str] = None
    configuration: Optional[ResourceConfiguration] = None
    configuration_schema: Optional[SchemaRef] = None

    button: Optional[ResourceButton] = None
    bridge_id: Optional[str] = None

    dependees: Optional[list[ResourceConfigurationDepends]] = None
    enabled: Optional[bool] = None
    last_error: Optional[str] = None

    state_schema: Optional[SchemaRef] = None
    supported_features: Optional[list[str]] = None  # TODO: Enum
    trigger_schema: Optional[SchemaRef] = None
    version: Optional[str] = None  # TODO Symantic Version

    is_configured: Optional[bool] = None

    migrated_from: Optional[str] = None
    script_id: Optional[UUID] = None
    description: Optional[str] = None
    id: UUID
    name: Optional[str] = None
    id_v1: Optional[str] = None
    locations: Optional[ResourceLocation] = None
    channels: Optional[list[ResourceChannel]] = None
    light_services: Optional[list[ResourceService]] = None
    stream_proxy: Optional[ResourceStreamProxy] = None
    mac_address: Optional[str] = None  # TODO: Make MAC Address
    identify: Optional[dict[str, str]] = None
    metadata: Optional[ResourceMetadata] = None
    mode: Optional[str] = None
    motion: Optional[ResourceMotion] = None
    light: Optional[ResourceLight] = None
    on: Optional[ResourceOn] = None
    owner: Optional[ResourceService] = None
    power_state: Optional[ResourcePowerState] = None
    time_zone: Optional[ResourceTimeZone] = None
    proxy: Optional[bool] = None
    rederer: Optional[bool] = None
    segments: Optional[ResourceSegments] = None
    signaling: Optional[dict[str, str]] = None
    product_data: Optional[ResourceProductData] = None
    services: Optional[list[ResourceService]] = None
    status: Optional[str] = None  # TODO: make enum
    type: ResourceType
