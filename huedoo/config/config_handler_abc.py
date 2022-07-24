from abc import ABC, abstractmethod
from typing import Any, Optional

from huedoo.config.config_model import ConfigModel


class ConfigHandlerABC(ABC):
    """
    Getters/Setters for Bridge Config
    """
    data: ConfigModel

    @abstractmethod
    def load(self) -> ConfigModel:
        """
        Load the ConfigModel
        """

    @abstractmethod
    def write(self, data_update: Optional[dict[str, Any]] = None, **kwargs):
        """
        Save the ConfigModel
        """
