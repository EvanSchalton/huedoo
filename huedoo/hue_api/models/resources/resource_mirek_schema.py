from pydantic import BaseModel  # type:ignore


class ResourceMirekSchema(BaseModel):
    mirek_maximum: int
    mirek_minimum: int
