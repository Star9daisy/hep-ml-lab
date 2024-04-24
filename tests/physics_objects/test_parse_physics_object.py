import pytest

from hml.physics_objects import (
    Collective,
    Multiple,
    Nested,
    Single,
    parse_physics_object,
)


def test_parse(
    single_names,
    collective_names,
    nested_names,
    multiple_names,
):
    for case in single_names:
        assert isinstance(parse_physics_object(case), Single)

    for case in collective_names:
        assert isinstance(parse_physics_object(case), Collective)

    for case in nested_names:
        assert isinstance(parse_physics_object(case), Nested)

    for case in multiple_names:
        assert isinstance(parse_physics_object(case), Multiple)

    with pytest.raises(ValueError):
        parse_physics_object("jet0_jet1")

    for case in multiple_names:
        assert isinstance(parse_physics_object(case), Multiple)

    with pytest.raises(ValueError):
        parse_physics_object("jet0_jet1")
