from pydantic import BaseModel  # type:ignore


class ResourceLight(BaseModel):
    light_level: int
    light_level_valid: bool

    class Config:
        use_enum_values = False
