from pydantic import BaseModel

class ResourceEffects(BaseModel):
    effect_values: list[str]
    status: str
    status_values: list[str]


