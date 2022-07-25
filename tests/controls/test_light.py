import pytest
from time import sleep

from uuid import UUID
from huedoo.bridge import Bridge
from huedoo.config.config_handler_abc import ConfigHandlerABC
from huedoo.config.config_handler_json import ConfigHandlerJson
from huedoo.hue_api.models import ResourceType

from huedoo.controls import Light
from huedoo.hue_api.routes import DeviceSetting


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
def test_light(test_bridge):
    return test_bridge.get_device(
        resource_type=ResourceType.LIGHT,
        id=LIGHT_UUID
    )


def test_light_can_adjust_brightness(test_light):
    starting_position: bool = test_light.is_on
    starting_brightness: float = test_light.brightness

    # Step 1
    target_brightness: float = 25
    test_light.set_brightness(
        target_brightness,
        force_on=True
    )
    default_sleep()
    assert test_light.is_on
    assert abs(test_light.brightness - target_brightness) < 1

    # Step 2
    target_brightness: float = 50
    test_light.set_brightness(
        target_brightness,
        force_on=True
    )
    default_sleep()
    assert test_light.is_on
    assert abs(test_light.brightness - target_brightness) < 1

    # Step 3
    target_brightness: float = 75
    test_light.set_brightness(
        target_brightness,
        force_on=True
    )
    default_sleep()
    assert test_light.is_on
    assert abs(test_light.brightness - target_brightness) < 1

    # Step 4
    target_brightness: float = 100
    test_light.set_brightness(
        target_brightness,
        force_on=True
    )
    default_sleep()
    assert test_light.is_on
    assert abs(test_light.brightness - target_brightness) < 1

    # Step 5 Toggle back
    if starting_position:
        test_light.set_brightness(
            starting_brightness,
            force_on=True
        )
    else:
        test_light.turn_off(
            DeviceSetting.BRIGHTNESS(starting_brightness),
        )

    default_sleep()
    assert test_light.is_on == starting_position
    assert abs(test_light.brightness - starting_brightness) < 1


def test_light_can_turn_on_and_off(test_light):
    starting_position: bool = test_light.is_on
    starting_brightness: float = test_light.brightness

    # Step 1 Toggle
    if starting_position:
        test_light.turn_off()
    else:
        test_light.turn_on()

    default_sleep()
    assert test_light.is_on != starting_position

    # Step 2 Toggle back
    if starting_position:
        test_light.turn_on()
    else:
        test_light.turn_off()

    default_sleep()
    assert test_light.is_on == starting_position
    assert abs(test_light.brightness - starting_brightness) < 1


def test_can_create_light_from_id(test_bridge):
    light = Light(id=LIGHT_UUID, bridge=test_bridge)
    assert light.resource.metadata.name == LIGHT_NAME


def test_can_create_light_from_name(test_bridge):
    light = Light(name=LIGHT_NAME, bridge=test_bridge)
    assert light.resource.id == LIGHT_UUID
