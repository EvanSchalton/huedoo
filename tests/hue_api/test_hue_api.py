import pytest
from huedoo.hue_api import HueAPI, HueAPIVersion
# import ipaddress

TEST_APP_NAME = "python_hue"
TEST_APP_TOKEN = "4MaXXNV6vALh2rNvtnYKh40PDNtbqVbhNlx68kLW"
TEST_IP_ADDRESS = "192.168.212.73"


# def test_can_get_ip_address():
#     # TODO: Figure out how to test this without getting rate limited
#     api = HueAPI()
#     # ip_address = api.get_bridge_ip()
#     # assert ipaddress.ip_address(ip_address)

#     assert hasattr(api, "get_bridge_ip")


def test_creates_endpoint_from_ip_address():
    """
    Given an ip_address derives the bridge's api path
    """
    api = HueAPI(TEST_IP_ADDRESS)
    assert api.get_uri(
        HueAPIVersion.V2) == f"https://{TEST_IP_ADDRESS}/clip/v2"
    assert api.get_uri(HueAPIVersion.V1) == f"https://{TEST_IP_ADDRESS}"


def test_ip_address_is_validated():
    """
    The IP address must be a valid v4 or v6 ip address
    """
    # TODO: Raise custom exception
    with pytest.raises(ValueError):
        HueAPI("test-ip-address")


def test_registering_sets_the_session_header(mocker):
    mocker.patch(
        'huedoo.hue_api.hue_api.HueAPI._get_app_token',
        return_value=TEST_APP_TOKEN
    )

    api = HueAPI(TEST_IP_ADDRESS)
    # testing the mock
    assert api._get_app_token(TEST_APP_NAME) == TEST_APP_TOKEN

    api.register_app(TEST_APP_NAME)  # does set the header
    assert api.session.headers['hue-application-key'] == TEST_APP_TOKEN
