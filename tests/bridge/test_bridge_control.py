from uuid import UUID
from time import sleep
import pytest

from huedoo.hue_api.models import ResourceType
from huedoo.config.config_handler_abc import ConfigHandlerABC
from huedoo.config import ConfigHandlerJson
from huedoo import Bridge, Light
from huedoo.hue_api.routes import DeviceSetting

# TODO: Should be config values
TEST_APP_NAME = "python_hue"
TEST_APP_TOKEN = "4MaXXNV6vALh2rNvtnYKh40PDNtbqVbhNlx68kLW"
TEST_BRIDGE_IP = "192.168.212.73"

LIGHT_NAME = "Living Room Right"
LIGHT_UUID = UUID('6ca4b771-2f4c-4b95-8b7f-bcc654eff84d')


def default_sleep():
    SLEEP_SECONDS = 1
    sleep(SLEEP_SECONDS)


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


def test_bridge_can_return_lights(test_bridge):
    lights = test_bridge.lights
    assert isinstance(lights, list)
    assert len(lights) > 0
    for i in lights:
        assert isinstance(i, Light)


def test_bridge_can_retrieve_a_device_by_id(test_bridge):
    light = test_bridge.get_device(
        resource_type=ResourceType.LIGHT,
        id=LIGHT_UUID
    )

    assert isinstance(light, Light)
    assert light.resource.type == ResourceType.LIGHT


def test_bridge_can_set_device(test_bridge):
    test_light = test_bridge.get_device(
        resource_type=ResourceType.LIGHT,
        id=LIGHT_UUID
    )
    starting_position = test_light.is_on

    # PART 1
    # toggle the light
    test_bridge.set_device(
        resource_type=ResourceType.LIGHT,
        id=LIGHT_UUID,
        device_settings=[
            DeviceSetting.TURN_OFF if starting_position else DeviceSetting.TURN_ON
        ]
    )

    default_sleep()

    # refresh resource
    test_light.refresh()
    assert test_light.is_on != starting_position

    # PART 2
    # toggle the light back
    test_bridge.set_device(
        resource_type=ResourceType.LIGHT,
        id=LIGHT_UUID,
        device_settings=[
            DeviceSetting.TURN_ON if starting_position else DeviceSetting.TURN_OFF

        ]
    )

    default_sleep()

    # refresh resource
    test_light.refresh()
    assert test_light.is_on == starting_position
