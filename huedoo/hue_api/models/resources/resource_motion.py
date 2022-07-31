from pydantic import BaseModel  # type:ignore


class ResourceMotion(BaseModel):
    motion: bool
    motion_valid: bool

    class Config:
        use_enum_values = False
