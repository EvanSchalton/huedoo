from pydantic import BaseModel


class ResourceLight(BaseModel):
    light_level: int
    light_level_valid: bool
