import pytest

from hml.physics_objects import Collective, Multiple, Nested, Single, parse


def test_parse(
    single_names,
    collective_names,
    nested_names,
    multiple_names,
):
    assert parse(None) is None

    for case in single_names:
        assert isinstance(parse(case), Single)
        assert isinstance(parse(Single.from_name("jet0")), Single)

    for case in collective_names:
        assert isinstance(parse(case), Collective)
        assert isinstance(parse(Collective.from_name("jet")), Collective)

    for case in nested_names:
        assert isinstance(parse(case), Nested)
        assert isinstance(parse(Nested.from_name("jet0.constituents:3")), Nested)

    for case in multiple_names:
        assert isinstance(parse(case), Multiple)
        assert isinstance(
            parse(Multiple.from_name("jet0,jet,jet0.constituents:3")), Multiple
        )

    with pytest.raises(ValueError):
        parse("jet0_jet1")
