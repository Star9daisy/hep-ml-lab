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

    assert str(obj) == "jet0"
    assert repr(obj) == "Single(branch='jet', index=0)"


def test_class_methods():
    obj = Single(branch="jet", index=0)

    assert obj.config == Single.from_name("jet0").config
    assert obj.config == Single.from_config(obj.config).config

    with pytest.raises(ValueError):
        Single.from_name("jet")

    with pytest.raises(ValueError):
        Single.from_config({"branch": "jet"})


def test_is_single():
    assert is_single(Single(branch="jet", index=0)) is True

    assert is_single("jet0") is True

    assert is_single("jet") is False
    assert is_single("jet:") is False
    assert is_single("jet1:") is False
    assert is_single("jet:5") is False
    assert is_single("jet1:5") is False

    assert is_single("jet0.constituents0") is False
    assert is_single("jet.constituents") is False
    assert is_single("jet1:.constituents1:") is False
    assert is_single("jet:5.constituents:5") is False
    assert is_single("jet1:5.constituents1:5") is False

    assert is_single(None) is False
