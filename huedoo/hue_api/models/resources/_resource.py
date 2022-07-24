from enum import Enum
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

from .resource_type import ResourceType
from .resource_service import ResourceService
from .resource_metadata import ResourceMetadata
from .resource_product_data import ResourceProductData
from .alert_action_value import AlertActionValue


class ResourceAlert(BaseModel):
    action_values: list[AlertActionValue]


class GamutColor(Enum):
    BLUE = "blue"
    GREEN = "green"
    RED = "red"


class ResourceColorGamut(BaseModel):
    x: float
    y: float


class GamutType(Enum):
    C = "C"


class ResourceColor(BaseModel):
    gamut: Optional[dict[GamutColor, ResourceColorGamut]] = None
    gamut_type: Optional[GamutType] = None
    xy: Optional[ResourceColorGamut] = None


class ResourceMirekSchema(BaseModel):
    mirek_maximum: int
    mirek_minimum: int


class ResourceColorTemperature(BaseModel):
    mirek: Optional[int]
    mirek_schema: Optional[ResourceMirekSchema] = None
    mirek_valid: Optional[bool] = None


class ResourceDimming(BaseModel):
    brightness: float
    min_dim_level: Optional[float] = None


class ResourceDynamics(BaseModel):
    speed: Optional[float] = None
    speed_valid: Optional[bool] = None
    status: Optional[str] = None
    status_values: Optional[list[str]] = None


class ResourceEffects(BaseModel):
    effect_values: list[str]
    status: str
    status_values: list[str]


class ResourceOn(BaseModel):
    on: bool


class ResourceSegmentItem(BaseModel):
    length: int
    start: int


class ResourceSegments(BaseModel):
    configurable: bool
    max_segments: int
    segments: list[ResourceSegmentItem]


class TimeZone(Enum):
    NEW_YORK = "America/New_York"


class ResourceTimeZone(BaseModel):
    time_zone: TimeZone


class ResourceButton(BaseModel):
    last_event: str  # TODO: Enum


class ResourcePowerState(BaseModel):
    battery_level: int
    battery_state: str  # TODO: ENUM normal/low


class ResourceMotion(BaseModel):
    motion: bool
    motion_valid: bool


class ResourceLight(BaseModel):
    light_level: int
    light_level_valid: bool


class Location(BaseModel):
    x: float
    y: float
    z: float


class ServiceLocation(BaseModel):
    positions: list[Location]
    service: ResourceService
    position: Location


class ResourceLocation(BaseModel):
    service_locations: list[ServiceLocation]


class ChannelMember(BaseModel):
    index: int
    service: ResourceService


class ResourceChannel(BaseModel):
    channel_id: int
    position: Location
    members: list[ChannelMember]


class ResourceStreamProxy(BaseModel):
    mode: str  # TODO: Enum
    node: ResourceService


class ResourceConfigurationWhat(BaseModel):
    group: ResourceService
    recall: ResourceService


class ResourceConfigurationWhere(BaseModel):
    group: ResourceService


class ResourceConfigurationWhenConstrained(BaseModel):
    type: str


class ResourceConfigurationDepends(BaseModel):
    level: str  # TODO: Enum
    target: ResourceService
    type: str


class ResourceConfiguration(BaseModel):
    end_scene: Optional[ResourceService] = None
    end_state: Optional[str] = None  # TODO: Enum
    what: Optional[list[ResourceConfigurationWhere]] = None
    where: list[ResourceConfigurationWhere]
    when_constrained: Optional[ResourceConfigurationWhenConstrained] = None
    # dependees: Optional[list[ResourceConfigurationDepends]] = None


class SchemaRef(BaseModel):
    ref: Optional[str] = Field(alias="$ref", default=None)


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
