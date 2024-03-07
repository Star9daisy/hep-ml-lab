import pytest

from hml.physics_objects import Collective, Nested, Single, is_nested


def test_init():
    obj = Nested(main=Single("jet", 0), sub="constituents1:3")

    assert obj.main == Single(branch="jet", index=0)
    assert obj.sub == Collective(branch="constituents", start=1, stop=3)

    assert obj.branch == "jet.constituents"
    assert obj.slices == [slice(0, 1), slice(1, 3)]
    assert obj.name == "jet0.constituents1:3"
    assert obj.config == {"main": "jet0", "sub": "constituents1:3"}


def test_special_methods():
    obj = Nested(main="jet0", sub="constituents1:3")

    assert obj == Nested(main="jet0", sub="constituents1:3")
    assert str(obj) == "jet0.constituents1:3"
    assert repr(obj) == "Nested(main='jet0', sub='constituents1:3')"


def test_class_methods():
    obj = Nested(main="jet0", sub="constituents1:3")

    assert obj == Nested.from_name("jet0.constituents1:3")
    assert obj == Nested.from_config(obj.config)

    with pytest.raises(ValueError):
        Nested.from_name("jet0")


def test_is_nested(single_names, collective_names, nested_names):
    assert is_nested(None) is False

    assert is_nested(Nested(main="jet0", sub="constituents1:3")) is True

    for case in nested_names:
        assert is_nested(case) is True

    for case in single_names:
        assert is_nested(case) is False

    for case in collective_names:
        assert is_nested(case) is False
