from huedoo.hue_api.exceptions.bridge_pairing import BridgeButtonNotPushed
import pytest

from huedoo.config.config_handler_abc import ConfigHandlerABC
from huedoo.config import ConfigHandlerJson
from huedoo.hue_api.hue_api import HueAPI
from huedoo import Bridge

TEST_APP_NAME = "python_hue"
TEST_APP_TOKEN = "4MaXXNV6vALh2rNvtnYKh40PDNtbqVbhNlx68kLW"
TEST_BRIDGE_IP = "192.168.212.73"


@pytest.fixture
def config_dir() -> str:
    return "/workspaces/huedoo/tests/test_data"


@pytest.fixture
def config_file() -> str:
    return "test-config.json"


@pytest.fixture
def test_config(config_dir, config_file) -> ConfigHandlerABC:
    config = ConfigHandlerJson(config_dir, config_file)
    config.write(
        app_name=TEST_APP_NAME,
        app_token=TEST_APP_TOKEN,
        ip_address=TEST_BRIDGE_IP
    )


@pytest.fixture
def test_bridge(test_config) -> Bridge:
    return Bridge(test_config)


@pytest.fixture
def test_config(config_dir, config_file) -> ConfigHandlerABC:
    config = ConfigHandlerJson(config_dir, config_file)
    config.write(ip_address=TEST_BRIDGE_IP)

    return config


def test_can_find_bridge_without_ip(test_config):
    """
    Bridge implements ip address lookup
    """
    # TODO: Figure out how to test this without getting rate limited
    test_config.data.ip_address = None
    bridge = Bridge(test_config)
    # ip_address = api.get_bridge_ip()
    # assert ipaddress.ip_address(ip_address)

    assert hasattr(bridge, "lookup_ip_address")


def test_bridge_ip_is_validated(test_config):
    """
    The IP address must be a valid v4 or v6 ip address
    """
    # TODO: Raise custom exception
    test_config.data.ip_address = "test-ip-address"
    with pytest.raises(ValueError):
        Bridge(test_config)


def test_bridge_has_api_ref(test_config):
    """
    Creating a bridge creates a connection to the HueAPI
    """
    bridge = Bridge(test_config)

    assert isinstance(bridge.api, HueAPI)


def test_bridge_registration_requires_button_push(test_bridge):
    """
    Raises exception if buttion isn't pressed
    """

    with pytest.raises(BridgeButtonNotPushed):
        test_bridge.register(TEST_APP_NAME)


def test_bridge_can_register_app(test_bridge, mocker):
    """
    App can be registered with the bridge
    """
    MOCK_TOKEN = "MOCK_TOKEN"
    mocker.patch(
        'huedoo.hue_api.hue_api.HueAPI._get_app_token',
        return_value=MOCK_TOKEN
    )
    test_bridge.register(TEST_APP_NAME)

    # print(test_bridge.config_handler.data)
    # print(test_bridge.config_handler.data.dict())

    assert test_bridge.config_handler.data.app_name == TEST_APP_NAME
    assert test_bridge.config_handler.data.app_token == MOCK_TOKEN
