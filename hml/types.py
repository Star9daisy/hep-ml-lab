from pathlib import Path
from typing import Literal
from typing import Union

PathLike = Union[str, Path]
CutLayerTopologies = Literal["parallel", "sequential"]


class VariableInteger(int):
    """A variable integer that represents any integer."""

    def __repr__(self):
        return "var"

    def __eq__(self, other: int):
        if not isinstance(other, int):
            raise TypeError(f"Cannot compare VariableInteger to {type(other)}")

        return True


class Generator:
    ...


class Representation:
    ...


class Dataset:
    ...


class Approach:
    ...


class Metric:
    ...
