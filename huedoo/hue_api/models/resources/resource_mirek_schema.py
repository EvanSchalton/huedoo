from pydantic import BaseModel


class ResourceMirekSchema(BaseModel):
    mirek_maximum: int
    mirek_minimum: int
