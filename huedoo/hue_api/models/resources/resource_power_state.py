from pydantic import BaseModel


class ResourcePowerState(BaseModel):
    battery_level: int
    battery_state: str  # TODO: ENUM normal/low
