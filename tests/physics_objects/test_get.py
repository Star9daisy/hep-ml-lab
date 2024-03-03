import pytest

from hml.physics_objects import Collective, Nested, Single, get


def test_get_physics_object(
    single_names,
    collective_names,
    nested_names,
):
    assert get(None) is None

    for case in single_names:
        assert isinstance(get(case), Single)

    for case in collective_names:
        assert isinstance(get(case), Collective)

    for case in nested_names:
        assert isinstance(get(case), Nested)

    with pytest.raises(ValueError):
        get("jet0,jet1")
