import pytest

from hml.validators import validate_type


@pytest.mark.parametrize("object_", ["string"])
@pytest.mark.parametrize("expected_types", [str, (str, int)])
def test_validate_type_good(object_, expected_types):
    validate_type(object_, expected_types)


@pytest.mark.parametrize("object_", ["string"])
@pytest.mark.parametrize("expected_types", [int, (int, float)])
def test_validate_type_bad(object_, expected_types):
    with pytest.raises(TypeError):
        validate_type(object_, expected_types)
