from __future__ import annotations

from math import nan
from typing import Any

import awkward as ak
import numpy as np

from ..physics_objects import ALL_OBJECTS_DICT
from ..physics_objects import get
from ..physics_objects.multiple import is_multiple


class Observable:
    ALL_OBSERVABLES = {}

    def __init__(
        self,
        physics_object: str | None = None,
        supported_types: list[str] | None = None,
        name: str | None = None,
        value: Any = None,
        dtype: Any = None,
    ):
        if physics_object is not None and supported_types is not None:
            self._validate_physics_object(physics_object, supported_types)

        self.physics_object = get(physics_object) if physics_object else None
        self.supported_types = supported_types
        self.name = name if name else self.__class__.__name__
        self.value = value if value else nan
        self.dtype = dtype if dtype else "float64"

    def read(self, entry) -> Any:
        raise NotImplementedError

    @property
    def shape(self):
        return str(self.to_awkward().type)

    @property
    def identifier(self) -> str:
        if self.physics_object:
            return f"{self.physics_object.identifier}.{self.name}"

        return self.name

    @property
    def config(self) -> dict[str, Any]:
        return {
            "physics_object": self.physics_object.identifier,
            "supported_types": self.supported_types,
            "name": self.name,
            "value": self.value,
            "dtype": self.dtype,
        }

    def __repr__(self) -> str:
        return self.identifier

    @classmethod
    def from_identifier(cls, identifier: str, **kwargs) -> Observable:
        if "." in identifier:
            physics_object, name = identifier.split(".")
        else:
            physics_object, name = None, identifier

        kwargs["physics_object"] = physics_object
        kwargs["name"] = name

        return cls(**kwargs)

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> Observable:
        return cls(**config)

    def to_awkward(self, dtype=None):
        value = self.value if isinstance(self.value, list) else [self.value]
        dtype = dtype if dtype is not None else self.dtype

        ak_array = ak.from_iter(value)
        ak_array = ak.values_astype(ak_array, dtype)
        try:
            ak_array = ak.to_regular(ak_array)
        except ValueError:
            pass
        return ak_array

    def to_numpy(self, dtype=None):
        dtype = dtype if dtype is not None else self.dtype
        value = self.value if isinstance(self.value, list) else [self.value]

        return np.array(value, dtype=dtype)

    def _validate_physics_object(
        self,
        identifier: str,
        supported_types: list[str],
    ) -> bool:
        # Avoid the remove method to modify the original list
        supported_types = supported_types.copy()

        if "multiple" in supported_types:
            supported_types.remove("multiple")

            if not is_multiple(identifier, supported_types):
                raise ValueError(
                    f"{identifier} is not a valid identifier for a multiple physics object."
                )

        else:
            obj = get(identifier)
            supported_classes = [ALL_OBJECTS_DICT[i] for i in supported_types]
            if type(obj) not in supported_classes:
                raise ValueError(
                    f"Physics object {obj} is not supported."
                    f"It is type {type(obj)} but should be one of {supported_types}"
                )

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        Observable.ALL_OBSERVABLES[cls.__name__] = cls

    @classmethod
    def add_alias(cls, *alias: str) -> None:
        for i in alias:
            Observable.ALL_OBSERVABLES[i] = cls
