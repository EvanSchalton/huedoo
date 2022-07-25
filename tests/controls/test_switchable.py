import pytest
from time import sleep

from uuid import UUID
from huedoo.bridge import Bridge
from huedoo.config.config_handler_abc import ConfigHandlerABC
from huedoo.config.config_handler_json import ConfigHandlerJson
from huedoo.hue_api.models import ResourceType, Resource

from huedoo.controls.base_classes import Switchable


def default_sleep():
    SLEEP_SECONDS = 1
    sleep(SLEEP_SECONDS)


# TODO: Should be config values
TEST_APP_NAME = "python_hue"
TEST_APP_TOKEN = "4MaXXNV6vALh2rNvtnYKh40PDNtbqVbhNlx68kLW"
TEST_BRIDGE_IP = "192.168.212.73"

LIGHT_NAME = "Living Room Right"
LIGHT_UUID = UUID('6ca4b771-2f4c-4b95-8b7f-bcc654eff84d')


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
    return config


@pytest.fixture
def test_bridge(test_config, mocker) -> Bridge:
    mocker.patch(
        'huedoo.hue_api.hue_api.HueAPI._get_app_token',
        return_value=TEST_APP_TOKEN
    )
    bridge = Bridge(test_config)
    bridge.api.setup_session()
    bridge.register(TEST_APP_NAME)

    return bridge


@pytest.fixture
def test_switchable(test_bridge):
    resource = test_bridge.api.get_device(
        resource_type=ResourceType.LIGHT,
        id=LIGHT_UUID
    )
    switchable = Switchable(
        resource=resource,
        bridge=test_bridge
    )
    return switchable


def test_switchable_can_turn_light_on_and_off(test_switchable):
    starting_position: bool = test_switchable.is_on

    # Step 1 Toggle
    if starting_position:
        test_switchable.turn_off()
    else:
        test_switchable.turn_on()

    default_sleep()
    assert test_switchable.is_on != starting_position

    # Step 2 Toggle back
    if starting_position:
        test_switchable.turn_on()
    else:
        test_switchable.turn_off()

    default_sleep()
    assert test_switchable.is_on == starting_position


def test_switchable_can_turn_off_light(test_switchable):
    test_switchable.turn_off()
    default_sleep()
    assert not test_switchable.is_on


def test_switchable_can_toggle_lights(test_switchable):
    starting_position = test_switchable.is_on

    test_switchable.toggle()
    default_sleep()
    assert test_switchable.is_on != starting_position

    test_switchable.toggle()
    default_sleep()
    assert test_switchable.is_on == starting_position
