import pytest

from hml.physics_objects.single import Single, is_single


def test_init():
    obj = Single(branch="jet", index=0)

    assert obj.branch == "jet"
    assert obj.index == 0
    assert obj.slices == [slice(0, 1)]
    assert obj.name == "jet0"
    assert obj.config == {"branch": "jet", "index": 0}


def test_special_methods():
    obj = Single(branch="jet", index=0)

    assert obj == Single(branch="jet", index=0)
    assert obj == "jet0"
    assert str(obj) == "jet0"
    assert repr(obj) == "Single(branch='jet', index=0)"


def test_class_methods():
    obj = Single(branch="jet", index=0)

    assert obj == Single.from_name("jet0")
    assert obj == Single.from_config(obj.config)

    with pytest.raises(ValueError):
        Single.from_name("jet")


def test_is_single(single_names, collective_names, nested_names):
    assert is_single(Single(branch="jet", index=0)) is True

    for case in single_names:
        assert is_single(case) is True

    for case in collective_names:
        assert is_single(case) is False

    for case in nested_names:
        assert is_single(case) is False
