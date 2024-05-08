import pytest

from hml.physics_objects import Collective, Nested, Single, is_nested


def test_init():
    obj = Nested(main="jet0", sub="constituents1:3")

    assert obj.main.name == "jet0"
    assert obj.sub.name == "constituents1:3"

    assert obj.branch == "jet.constituents"
    assert obj.slices == [slice(0, 1), slice(1, 3)]
    assert obj.name == "jet0.constituents1:3"
    assert obj.config == {"main": "jet0", "sub": "constituents1:3"}

    # Other cases
    obj = Nested(
        main=Single(branch="jet", index=0),
        sub=Collective(branch="constituents", start=1, stop=3),
    )
    assert obj.name == "jet0.constituents1:3"


def test_special_methods():
    obj = Nested(main="jet0", sub="constituents1:3")

    assert str(obj) == "jet0.constituents1:3"
    assert repr(obj) == "Nested(main='jet0', sub='constituents1:3')"


def test_class_methods():
    obj = Nested(main="jet0", sub="constituents1:3")

    assert obj.config == Nested.from_name("jet0.constituents1:3").config
    assert obj.config == Nested.from_config(obj.config).config

    with pytest.raises(ValueError):
        Nested.from_name("jet0")

    with pytest.raises(ValueError):
        Nested.from_config({"main": "jet0"})


def test_is_nested():
    assert is_nested(Nested(main="jet0", sub="constituents1:3")) is True

    assert is_nested("jet0") is False

    assert is_nested("jet") is False
    assert is_nested("jet:") is False
    assert is_nested("jet1:") is False
    assert is_nested("jet:5") is False
    assert is_nested("jet1:5") is False

    assert is_nested("jet0.constituents0") is True
    assert is_nested("jet.constituents") is True
    assert is_nested("jet1:.constituents1:") is True
    assert is_nested("jet:5.constituents:5") is True
    assert is_nested("jet1:5.constituents1:5") is True

    assert is_nested(None) is False
