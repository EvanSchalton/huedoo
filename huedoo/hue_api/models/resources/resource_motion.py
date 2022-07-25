from pydantic import BaseModel  # type:ignore


class ResourceMotion(BaseModel):
    motion: bool
    motion_valid: bool
