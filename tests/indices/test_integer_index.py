import pytest

from hml.indices.integer import IntegerIndex


def test_init():
    index = IntegerIndex()
    assert index.number == 0


def test_eq():
    index1 = IntegerIndex()
    index2 = IntegerIndex()
    assert index1 == index2

    index1 = IntegerIndex()
    index2 = IntegerIndex(1)
    assert index1 != index2


def test_repr():
    index = IntegerIndex()
    assert repr(index) == "IntegerIndex(number=0)"


def test_property_value():
    index = IntegerIndex(0)
    assert index.value == 0


def test_classmethod_from_int():
    index = IntegerIndex.from_int(0)
    assert index == IntegerIndex()


def test_property_name():
    index = IntegerIndex(0)
    assert index.name == "0"


def test_classmethod_from_name():
    with pytest.raises(ValueError):
        IntegerIndex.from_name("invalid")

    index = IntegerIndex.from_name("0")
    assert index == IntegerIndex()


def test_property_config():
    index = IntegerIndex(0)
    assert index.config == {"number": 0}


def test_classmethod_from_config():
    with pytest.raises(ValueError):
        IntegerIndex.from_config({"non_number": 0})

    index = IntegerIndex.from_config({"number": 0})
    assert index == IntegerIndex()
