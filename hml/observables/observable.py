from __future__ import annotations

from math import nan
from typing import Any

import awkward as ak
import numpy as np

from ..physics_objects import ALL_OBJECTS_DICT
from ..physics_objects import get_physics_object
from ..physics_objects.multiple import is_multiple


class Observable:
    ALL_OBSERVABLES = {}

    def __init__(
        self,
        physics_object: str | None = None,
        supported_types: list[str] | None = None,
    ):
        self._validate_physics_object(physics_object, supported_types)

        self.physics_object = get_physics_object(physics_object)
        self.supported_types = supported_types

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        Observable.ALL_OBSERVABLES[cls.__name__] = cls

    def __repr__(self) -> str:
        return f"{self.name} : {self.value}"

    def __eq__(self, other) -> bool:
        return self.config == other.config

    def read_ttree(self, entry) -> Any:
        raise NotImplementedError

    def to_awkward(self, dtype=None):
        value = self.value if isinstance(self.value, list) else [self.value]

        ak_array = ak.from_iter(value)
        ak_array = ak.values_astype(ak_array, dtype)
        try:
            ak_array = ak.to_regular(ak_array)
        except ValueError:
            pass
        return ak_array

    def to_numpy(self, dtype=None):
        value = self.value if isinstance(self.value, list) else [self.value]

        return np.array(value, dtype=dtype)

    @property
    def name(self):
        if self.physics_object is not None:
            return f"{self.physics_object.name}.{self.__class__.__name__}"
        else:
            return self.__class__.__name__

    @property
    def value(self):
        if hasattr(self, "_value"):
            return self._value
        else:
            return nan

    @property
    def shape(self):
        return str(self.to_awkward().type)

    @property
    def config(self) -> dict[str, Any]:
        if self.physics_object is not None:
            return {"physics_object": self.physics_object.name}
        else:
            return {}

    @classmethod
    def from_name(cls, name: str, **kwargs) -> Observable:
        if "." in name:
            physics_object = name.split(".")[0]
        else:
            physics_object = None

        return cls(physics_object, **kwargs)

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> Observable:
        return cls(**config)

    @classmethod
    def add_alias(cls, *alias: str) -> None:
        for i in alias:
            Observable.ALL_OBSERVABLES[i] = cls

    def _validate_physics_object(
        self,
        name: str | None,
        supported_types: list[str] | None,
    ) -> bool:
        if supported_types is None:
            return

        if name is None and supported_types is not None:
            raise ValueError(
                "If supported_types is provided, physics_object must also be provided."
            )

        # Avoid the remove method to modify the original list
        supported_types = supported_types.copy()

        if "multiple" in supported_types:
            supported_types.remove("multiple")

            if not is_multiple(name, supported_types):
                raise ValueError(
                    f"{name} is not a valid identifier for a multiple physics object."
                )

        else:
            obj = get_physics_object(name)
            supported_classes = [ALL_OBJECTS_DICT[i] for i in supported_types]
            if type(obj) not in supported_classes:
                raise ValueError(
                    f"Physics object {obj} is not supported."
                    f"It is type {type(obj)} but should be one of {supported_types}"
                )
