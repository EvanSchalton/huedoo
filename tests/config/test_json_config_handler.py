import pytest
from huedoo.config import ConfigHandlerJson, ConfigModel


@pytest.fixture
def config_dir() -> str:
    return "/workspaces/huedoo/tests/test_data"


@pytest.fixture
def config_file() -> str:
    return "config.json"


@pytest.fixture
def test_config(config_dir, config_file):
    return ConfigHandlerJson(config_dir, config_file)


def test_config_handler_json(config_dir, config_file):
    config = ConfigHandlerJson(config_dir, config_file)

    assert config._dir == config_dir
    assert config._file == config_file


def test_config_can_read_attribute(test_config):
    assert isinstance(test_config.data, ConfigModel)


def test_config_can_write_attribute(test_config):
    test_config.write({'hello': 'world'})
    assert test_config.data.hello == 'world'
