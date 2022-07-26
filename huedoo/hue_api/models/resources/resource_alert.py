from pydantic import BaseModel  # type:ignore
from .alert_action_value import AlertActionValue


class ResourceAlert(BaseModel):
    action_values: list[AlertActionValue]

    class Config:
        use_enum_values = False
