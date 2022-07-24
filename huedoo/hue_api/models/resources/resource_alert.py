from pydantic import BaseModel
from .alert_action_value import AlertActionValue


class ResourceAlert(BaseModel):
    action_values: list[AlertActionValue]
