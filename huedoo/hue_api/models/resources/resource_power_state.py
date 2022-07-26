from pydantic import BaseModel  # type:ignore


class ResourcePowerState(BaseModel):
    battery_level: int
    battery_state: str  # TODO: ENUM normal/low

    class Config:
        use_enum_values = False
