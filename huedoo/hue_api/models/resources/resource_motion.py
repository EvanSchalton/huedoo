from pydantic import BaseModel

class ResourceMotion(BaseModel):
    motion: bool
    motion_valid: bool


