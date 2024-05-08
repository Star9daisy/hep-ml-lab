import pytest

from hml.physics_objects import Collective, Nested, Single, get, parse_physics_object


def test_get():
    assert get("single") is Single
    assert get("Single") is Single
    assert get("collective") is Collective
    assert get("Collective") is Collective
    assert get("nested") is Nested
    assert get("Nested") is Nested


def test_parse():
    single_names = ["jet0", "muon1"]
    for case in single_names:
        assert isinstance(parse_physics_object(case), Single)

    collective_names = ["jet", "jet:", "jet1:", "jet:3", "jet1:3"]
    for case in collective_names:
        assert isinstance(parse_physics_object(case), Collective)

    nested_names = [
        "jet0.Constituents0",
        "jet0.Constituents:",
        "jet0.Constituents1:",
        "jet0.Constituents:3",
        "jet0.Constituents1:3",
        "jet:.Constituents:",
        "jet:.Constituents1:",
        "jet:.Constituents:3",
        "jet:.Constituents1:3",
        "jet1:.Constituents:",
        "jet1:.Constituents1:",
        "jet1:.Constituents:3",
        "jet1:.Constituents1:3",
        "jet:3.Constituents:",
        "jet:3.Constituents1:",
        "jet:3.Constituents:3",
        "jet:3.Constituents1:3",
        "jet1:3.Constituents:",
        "jet1:3.Constituents1:",
        "jet1:3.Constituents:3",
        "jet1:3.Constituents1:3",
    ]
    for case in nested_names:
        assert isinstance(parse_physics_object(case), Nested)

    with pytest.raises(ValueError):
        parse_physics_object("jet0_jet1")

    with pytest.raises(ValueError):
        parse_physics_object("jet0_jet1")
