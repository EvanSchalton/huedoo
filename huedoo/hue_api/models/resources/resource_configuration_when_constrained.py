from pydantic import BaseModel


class ResourceConfigurationWhenConstrained(BaseModel):
    type: str
