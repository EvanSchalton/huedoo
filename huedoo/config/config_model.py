from pydantic import BaseModel, Extra  # type:ignore
from ipaddress import IPv4Address, IPv6Address
from typing import Optional


class ConfigModel(BaseModel, extra=Extra.allow):
    """
    Hue Configuration Settings
    """
    ip_address: Optional[IPv4Address | IPv6Address]
