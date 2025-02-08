import re
from importlib import import_module
from typing import Any
from .index import Index
from .integer import IntegerIndex
from .range import RangeIndex

from typeguard import typechecked


IndexLike = int | slice | IntegerIndex | RangeIndex
BUILTIN_REGISTERABLE_CLASSES = [IntegerIndex, RangeIndex]


@typechecked
def index_like_to_index(index: IndexLike) -> Index:
    if isinstance(index, int):
        return IntegerIndex.from_int(index)
    elif isinstance(index, slice):
        return RangeIndex.from_slice(index)
    else:
        return index


@typechecked
def serialize(obj: IndexLike) -> dict[str, Any]:
    obj = index_like_to_index(obj)

    return {
        "module": obj.__module__,
        "class_name": obj.__class__.__name__,
        "config": obj.config,
    }


@typechecked
def deserialize(dict_: dict[str, Any]) -> Index:
    if "module" not in dict_ or "class_name" not in dict_ or "config" not in dict_:
        raise ValueError(
            f"Required 'module', 'class_name', and 'config' in the dictionary. "
            f"Received: {dict_=}"
        )

    module = import_module(dict_["module"])
    cls = getattr(module, dict_["class_name"])

    return cls.from_config(dict_["config"])


@typechecked
def retrieve(name: str) -> Index:
    for cls in BUILTIN_REGISTERABLE_CLASSES:
        if re.fullmatch(cls.PATTERN, name):
            return cls.from_name(name)

    raise ValueError(f"No index class corresponds to the name: {name=}")
