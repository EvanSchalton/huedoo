import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--trigger_lights",
        action="store_true",
        help="run the tests only in case of that command line (marked with marker @trigger_lights)"
    )


def pytest_runtest_setup(item):
    if 'trigger_lights' in item.keywords and not item.config.getoption("--trigger_lights"):
        pytest.skip("need --trigger_lights option to run this test")
