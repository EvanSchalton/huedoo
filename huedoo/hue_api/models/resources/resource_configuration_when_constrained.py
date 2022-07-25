from pydantic import BaseModel  # type:ignore


class ResourceConfigurationWhenConstrained(BaseModel):
    type: str
