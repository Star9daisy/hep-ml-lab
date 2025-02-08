import pytest

from hml.indices.range import RangeIndex


def test_init():
    index = RangeIndex()
    assert index.start is None
    assert index.stop is None

    index = RangeIndex(start=1, stop=10)
    assert index.start == 1
    assert index.stop == 10


def test_repr():
    index = RangeIndex()
    assert repr(index) == "RangeIndex(start=None, stop=None)"


def test_property_value():
    index = RangeIndex()
    assert index.value == slice(None, None)


def test_classmethod_from_slice():
    index = RangeIndex.from_slice(slice(None))
    assert index == RangeIndex()


def test_property_name():
    index = RangeIndex()
    assert index.name == ""

    index = RangeIndex(stop=10)
    assert index.name == ":10"

    index = RangeIndex(start=1)
    assert index.name == "1:"

    index = RangeIndex(start=1, stop=10)
    assert index.name == "1:10"


def test_classmethod_from_name():
    with pytest.raises(ValueError):
        RangeIndex.from_name("invalid")

    index = RangeIndex.from_name("")
    assert index == RangeIndex()

    index = RangeIndex.from_name("1:10")
    assert index == RangeIndex(start=1, stop=10)


def test_property_config():
    index = RangeIndex()
    assert index.config == {"start": None, "stop": None}


def test_classmethod_from_config():
    with pytest.raises(ValueError):
        RangeIndex.from_config({"non_start": None, "non_stop": None})

    index = RangeIndex.from_config({"start": None, "stop": None})
    assert index == RangeIndex()
