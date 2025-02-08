import pytest

from hml.indices import deserialize, index_like_to_index, retrieve, serialize
from hml.indices.integer import IntegerIndex
from hml.indices.range import RangeIndex


def test_index_like_to_index():
    index = index_like_to_index(0)
    assert index == IntegerIndex()

    index = index_like_to_index(slice(None))
    assert index == RangeIndex()

    index = index_like_to_index(IntegerIndex(0))
    assert index == IntegerIndex()


def test_serialize():
    index = IntegerIndex()
    assert serialize(index) == {
        "module": "hml.indices.integer",
        "class_name": "IntegerIndex",
        "config": {"number": 0},
    }

    index = RangeIndex()
    assert serialize(index) == {
        "module": "hml.indices.range",
        "class_name": "RangeIndex",
        "config": {"start": None, "stop": None},
    }


def test_deserialize():
    with pytest.raises(ValueError):
        deserialize({"non_module": ""})

    with pytest.raises(ValueError):
        deserialize({"non_class_name": ""})

    with pytest.raises(ValueError):
        deserialize({"non_config": {}})

    index = deserialize(
        {
            "module": "hml.indices.integer",
            "class_name": "IntegerIndex",
            "config": {"number": 0},
        }
    )
    assert index == IntegerIndex()

    index = deserialize(
        {
            "module": "hml.indices.range",
            "class_name": "RangeIndex",
            "config": {"start": None, "stop": None},
        }
    )
    assert index == RangeIndex()


def test_retrieve():
    with pytest.raises(ValueError):
        retrieve("invalid")

    index = retrieve("0")
    assert index == IntegerIndex()

    index = retrieve("")
    assert index == RangeIndex()
