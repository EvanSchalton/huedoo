from huedoo.utilities import Enum
from pydantic import BaseModel
import pytest
import json


class EnumTest(Enum):
    """
    Enum For Testing Purposes
    """
    A = "a"
    B = "b"
    C = "c"


class ModelTest(BaseModel):
    """
    Model for Testing Purposes
    """
    test_enum: EnumTest
    number: int


@pytest.fixture
def test_model() -> ModelTest:
    return ModelTest(
        test_enum=EnumTest.A,
        number=1
    )


def test_enum_is_enum(test_model):
    """
    The model should maintain an Enum
    """
    assert isinstance(test_model.test_enum, EnumTest)


def test_model_dict_has_enum_as_string(test_model):
    """
    The model.dict() should maintain enum
    """
    assert test_model.dict()['test_enum'] == test_model.test_enum


def test_model_json_has_enum_as_string(test_model):
    """
    The model.json() should work, unmarshal enum
    """
    assert json.loads(test_model.json())[
        'test_enum'] == test_model.test_enum.value
