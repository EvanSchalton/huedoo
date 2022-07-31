from pydantic import BaseModel  # type:ignore


class ResourceEffects(BaseModel):
    effect_values: list[str]
    status: str
    status_values: list[str]

    class Config:
        use_enum_values = False
