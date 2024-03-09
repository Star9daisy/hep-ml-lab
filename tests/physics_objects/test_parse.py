import pytest

from hml.physics_objects import Collective, Multiple, Nested, Single, parse


def test_parse(
    single_names,
    collective_names,
    nested_names,
    multiple_names,
):
    for case in single_names:
        assert isinstance(parse(case), Single)

    for case in collective_names:
        assert isinstance(parse(case), Collective)

    for case in nested_names:
        assert isinstance(parse(case), Nested)

    for case in multiple_names:
        assert isinstance(parse(case), Multiple)

    with pytest.raises(ValueError):
        parse("jet0_jet1")
