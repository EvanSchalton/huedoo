import pytest
from time import sleep
from uuid import UUID, uuid4

from huedoo.hue_api.hue_api import (
    HueAPI,
    ResourceType
)

TEST_APP_NAME = "python_hue"
TEST_APP_TOKEN = "4MaXXNV6vALh2rNvtnYKh40PDNtbqVbhNlx68kLW"
TEST_IP_ADDRESS = "192.168.212.73"

LIGHT_NAME = "Living Room Right"
LIGHT_UUID = UUID('6ca4b771-2f4c-4b95-8b7f-bcc654eff84d')


def default_sleep():
    SLEEP_SECONDS = 1
    sleep(SLEEP_SECONDS)


@pytest.fixture
def test_api(mocker) -> HueAPI:
    mocker.patch(
        'huedoo.hue_api.hue_api.HueAPI._get_app_token',
        return_value=TEST_APP_TOKEN
    )
    api = HueAPI(TEST_IP_ADDRESS)
    api.register_app(TEST_APP_NAME)
    return api


def test_bridge_can_list_all_resources(test_api):
    results = test_api._list_resources()
    assert len(results) > 0


def test_bridge_can_lookup_resource_by_id(test_api):
    result = test_api.get_device(
        resource_type=ResourceType.LIGHT, id=LIGHT_UUID)
    assert result.id == LIGHT_UUID
    assert result.metadata.name == LIGHT_NAME


def test_bridge_can_lookup_resource_by_name(test_api):
    result = test_api.get_device(
        resource_type=ResourceType.LIGHT, name=LIGHT_NAME)
    assert result.id == LIGHT_UUID
    assert result.metadata.name == LIGHT_NAME


def test_bridge_raises_exception_on_unknown_device(test_api):
    with pytest.raises(Exception):
        # TODO: Custom Error
        test_api.get_device(
            resource_type=ResourceType.LIGHT,
            name="FAKE LIGHT"
        )

    with pytest.raises(Exception):
        # TODO: Custom Error
        test_api.get_device(resource_type=ResourceType.LIGHT, id=uuid4())


def test_bridge_requires_name_or_id(test_api):
    with pytest.raises(Exception):
        # TODO: Custom Error
        test_api.get_device(resource_type=ResourceType.LIGHT)


def test_bridge_requires_name_or_id_not_both(test_api):
    with pytest.raises(Exception):
        # TODO: Custom Error
        test_api.get_device(
            resource_type=ResourceType.LIGHT,
            id=LIGHT_UUID,
            name=LIGHT_NAME
        )


def test_api_can_set_device(test_api):
    test_light = test_api.get_device(
        resource_type=ResourceType.LIGHT,
        id=LIGHT_UUID
    )
    starting_position: bool = test_light.on.on

    # PART 1
    # toggle the light
    test_api.set_device(
        resource_type=ResourceType.LIGHT,
        id=LIGHT_UUID,
        params={
            'on': {'on': not starting_position}
        }
    )

    default_sleep()

    # refresh resource
    test_light = test_api.get_device(
        resource_type=ResourceType.LIGHT,
        id=LIGHT_UUID
    )

    assert test_light.on.on != starting_position

    # PART 2
    # toggle the light back
    test_api.set_device(
        resource_type=ResourceType.LIGHT,
        id=LIGHT_UUID,
        params={
            'on': {'on': starting_position}
        }
    )

    default_sleep()

    # refresh resource
    test_light = test_api.get_device(
        resource_type=ResourceType.LIGHT,
        id=LIGHT_UUID
    )

    assert test_light.on.on == starting_position
