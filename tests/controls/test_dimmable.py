import pytest
from time import sleep

from uuid import UUID
from huedoo import Bridge
from huedoo.config.config_handler_abc import ConfigHandlerABC
from huedoo.config.config_handler_json import ConfigHandlerJson
from huedoo.hue_api.models import ResourceType
from huedoo.controls.base_classes import Dimmable
from huedoo.hue_api.routes import DeviceSetting


def default_sleep():
    SLEEP_SECONDS = 1.5
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
def test_dimmable(test_bridge):
    resource = test_bridge.api.get_device(
        resource_type=ResourceType.LIGHT,
        uuid=LIGHT_UUID
    )
    dimmable = Dimmable(
        resource=resource,
        bridge=test_bridge
    )
    return dimmable


@pytest.mark.trigger_lights
def test_dimmable_can_turn_light_on_and_off(test_dimmable):
    starting_position: bool = test_dimmable.is_on
    starting_brightness: float = test_dimmable.brightness

    # Step 1 Toggle
    target_brightness: float = starting_brightness
    if starting_position:
        test_dimmable.set_brightness(0)
    else:
        target_brightness = 75
        test_dimmable.set_brightness(target_brightness)

    default_sleep()
    assert test_dimmable.is_on != starting_position
    assert abs(test_dimmable.brightness - target_brightness) < 1

    # Step 2 Adjust Brightness
    target_brightness = 100
    test_dimmable.set_brightness(target_brightness, force_on=True)
    default_sleep()
    assert test_dimmable.is_on
    assert abs(test_dimmable.brightness - target_brightness) < 1

    # Step 3 Toggle back
    target_brightness = starting_brightness
    if starting_position:
        test_dimmable.set_brightness(
            target_brightness,
            force_on=True
        )
    else:
        test_dimmable.turn_off(
            DeviceSetting.BRIGHTNESS(target_brightness)
        )

    default_sleep()
    assert test_dimmable.is_on == starting_position
    assert abs(test_dimmable.brightness - target_brightness) < 1
