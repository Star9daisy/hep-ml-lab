import pytest

from hml.physics_objects.collective import Collective, is_collective


def test_init():
    obj = Collective(branch="jet", start=1, stop=3)

    assert obj.branch == "jet"
    assert obj.start == 1
    assert obj.stop == 3
    assert obj.slices == [slice(1, 3)]
    assert obj.name == "jet1:3"
    assert obj.config == {"branch": "jet", "start": 1, "stop": 3}

    # Other cases
    assert Collective(branch="jet").name == "jet"
    assert Collective(branch="jet", start=1).name == "jet1:"
    assert Collective(branch="jet", stop=3).name == "jet:3"


def test_special_methods():
    obj = Collective(branch="jet", start=1, stop=3)

    assert str(obj) == "jet1:3"
    assert repr(obj) == "Collective(branch='jet', start=1, stop=3)"


def test_class_methods():
    obj = Collective(branch="jet", start=1, stop=3)

    assert obj.config == Collective.from_name("jet1:3").config
    assert obj.config == Collective.from_config(obj.config).config

    with pytest.raises(ValueError):
        Collective.from_name("jet0")

    with pytest.raises(ValueError):
        Collective.from_config({"branch": "jet"})


def test_is_collective():
    assert is_collective(Collective(branch="jet", start=1, stop=3)) is True

    assert is_collective("jet0") is False

    assert is_collective("jet") is True
    assert is_collective("jet:") is True
    assert is_collective("jet1:") is True
    assert is_collective("jet:5") is True
    assert is_collective("jet1:5") is True

    assert is_collective("jet0.constituents0") is False
    assert is_collective("jet.constituents") is False
    assert is_collective("jet1:.constituents1:") is False
    assert is_collective("jet:5.constituents:5") is False
    assert is_collective("jet1:5.constituents1:5") is False

    assert is_collective(None) is False
