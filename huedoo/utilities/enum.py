from enum import Enum as BaseEnum


class Enum(BaseEnum):
    """
    A string-able enum
    """

    def _get_value(self, **kwargs) -> str:
        """
        Handles marshalling for pydantic
        """
        return self.value
