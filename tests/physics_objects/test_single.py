import pytest

from hml.physics_objects.single import Single
from hml.physics_objects.single import is_single


def test_init():
    obj = Single(branch="Jet", index=0)

    # Attributes ------------------------------------------------------------- #
    assert obj.branch == "Jet"
    assert obj.index == 0
    assert obj.name == "Jet0"
    assert obj.objects is None
    assert obj.config == {"branch": "Jet", "index": 0}


def test_special_methods():
    obj = Single(branch="Jet", index=0)

    # __eq__ ----------------------------------------------------------------- #
    assert Single(branch="Jet", index=0) == Single(branch="Jet", index=0)

    # __repr__ --------------------------------------------------------------- #
    assert repr(obj) == "Single(name='Jet0', objects=None)"


def test_class_methods():
    obj = Single(branch="Jet", index=0)

    # from_name -------------------------------------------------------------- #
    assert obj == Single.from_name("Jet0")

    # from_config ------------------------------------------------------------ #
    assert obj == Single.from_config(obj.config)


def test_read_ttree(event):
    # Common cases ----------------------------------------------------------- #
    obj = Single(branch="Jet", index=0).read_ttree(event)
    assert len(obj.objects) == 1

    obj = Single(branch="Constituents", index=0).read_ttree(event.Jet[0])
    assert len(obj.objects) == 1

    # Edge cases ------------------------------------------------------------- #
    obj = Single(branch="Jet", index=100).read_ttree(event)
    assert len(obj.objects) == 0

    obj = Single(branch="Constituents", index=100).read_ttree(event.Jet[0])
    assert len(obj.objects) == 0

    # Error cases ------------------------------------------------------------ #
    with pytest.raises(ValueError):
        Single(branch="Unknown", index=0).read_ttree(event)


def test_is_single(single_names, collective_names, nested_names, multiple_names):
    # Valid cases ------------------------------------------------------------ #
    for case in single_names:
        assert is_single(case) is True

    # Invalid cases ---------------------------------------------------------- #
    for case in collective_names:
        assert is_single(case) is False

    for case in nested_names:
        assert is_single(case) is False

    for case in multiple_names:
        assert is_single(case) is False
