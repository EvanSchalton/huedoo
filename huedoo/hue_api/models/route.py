from pydantic import BaseModel, root_validator  # type:ignore
from typing import Any, Optional
from .request_method import RequestMethod
from .hue_api_version import HueAPIVersion
from string import Template


class Route(BaseModel):
    """
    Defines a configuration for a hue route
    """
    mode: RequestMethod = RequestMethod.GET
    api_version: HueAPIVersion = HueAPIVersion.V2
    path: str | Template = Template("/api")
    verify: bool = True
    parameters: Optional[dict[str, Any]] = None

    class Config:
        use_enum_values = False

    class Config:
        arbitrary_types_allowed = True
        allow_reuse = True

    @property
    def endpoint(self) -> str:
        """
        Returns the endpoint as a string
        """
        parameters = self.parameters
        if parameters is None:
            parameters = {}

        return self.path.substitute(**parameters)

    @root_validator
    def validate(cls, values):  # type:ignore
        """
        Converst str to Templates
        """
        if isinstance(values.get('path'), Template):
            return values
        else:
            values['path'] = Template(values.get('path'))
        return values
