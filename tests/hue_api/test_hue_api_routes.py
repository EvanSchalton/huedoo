from huedoo.hue_api.hue_api import HueAPI
import pytest

TEST_APP_NAME = "python_hue"
TEST_APP_TOKEN = "4MaXXNV6vALh2rNvtnYKh40PDNtbqVbhNlx68kLW"
TEST_IP_ADDRESS = "192.168.212.73"


def test_bridge_can_list_all_resources(mocker):

    mocker.patch(
        'huedoo.hue_api.hue_api.HueAPI._get_app_token',
        return_value=TEST_APP_TOKEN
    )
    api = HueAPI(TEST_IP_ADDRESS)
    api.register_app(TEST_APP_NAME)

    results = api._list_resources()
    assert len(results) > 0
