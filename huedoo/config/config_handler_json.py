from typing import Any, Optional
from .config_handler_abc import ConfigHandlerABC
from .config_model import ConfigModel
import json
import os
from ipaddress import IPv4Address, IPv6Address


class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (IPv4Address, IPv6Address)):
            return str(o)
        return json.JSONEncoder.default(self, o)


class ConfigHandlerJson(ConfigHandlerABC):
    """
    Reads/Writes configs to json file
    """
    data: ConfigModel

    def __init__(self, config_dir, config_file):
        self._dir = config_dir
        self._file = config_file

        self.load()

    def load(self):
        """
        Load the config from the json file
        """
        filepath = os.path.join(self._dir, self._file)

        if os.path.exists(filepath):
            with open(filepath, encoding="utf-8") as in_config:
                config_json = json.load(in_config)
                # print("config_json:", config_json)
                self.data = ConfigModel(**config_json)
            return
        self.data = ConfigModel()

    def write(self, data_update: Optional[dict[str, Any]] = None, **kwargs):
        """
        Write the kwargs to the model
        """
        if data_update is None:
            data_update = {}

        config_data = {**self.data.dict(), **data_update, **kwargs}

        with open(
            os.path.join(self._dir, self._file),
            "w+",
            encoding="utf-8"
        ) as out_config:
            # print("config_data:", config_data)
            out_config.write(json.dumps(
                config_data, indent=2, cls=CustomEncoder))

        self.data = ConfigModel(**config_data)
