from pydantic import BaseModel  # type:ignore


class ResourceConfigurationWhenConstrained(BaseModel):
    type: str

    class Config:
        use_enum_values = False
