from __future__ import annotations

import awkward as ak
import numpy as np

from .. import physics_objects
from ..physics_objects import PhysicsObject
from .observable_utils import branches_to_momentum4d, get_constituents

ALL_OBJECTS_DICT = {}


class Observable:
    def __init__(
        self,
        physics_object: str | PhysicsObject | None = None,
        class_name: str | None = None,
    ) -> None:
        self.physics_object = physics_object
        self.class_name = class_name

        self.value = None

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        ALL_OBJECTS_DICT[cls.__name__] = cls

    def __eq__(self, other: str | Observable) -> bool:
        if isinstance(other, str):
            other = self.from_name(other)

        return (
            self.physics_object == other.physics_object
            and self.__class__ == other.__class__
        )

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"{self.name}: {self.value.type!s}"

    @classmethod
    def add_alias(cls, *alias: str) -> None:
        for i in alias:
            ALL_OBJECTS_DICT[i] = cls

    @classmethod
    def from_name(cls, name: str, **kwargs) -> "Observable":
        *parts, class_name = name.split(".")

        if class_name not in ALL_OBJECTS_DICT:
            raise ValueError(
                f"Invalid class name '{class_name}' for the observable {cls.__name__}"
            )
        elif ALL_OBJECTS_DICT[class_name] != cls:
            raise ValueError(
                f"Invalid class name '{class_name}' for the observable {cls.__name__}"
            )

        physics_object = ".".join(parts) if len(parts) > 0 else None

        return cls(physics_object, class_name, **kwargs)

    @classmethod
    def from_config(cls, config: dict) -> "Observable":
        return cls(**config)

    @property
    def physics_object(self) -> PhysicsObject | None:
        return self._physics_object

    @physics_object.setter
    def physics_object(self, physics_object: str | PhysicsObject | None) -> None:
        if isinstance(physics_object, PhysicsObject):
            self._physics_object = physics_object
        else:
            self._physics_object = physics_objects.parse(physics_object)

    @property
    def class_name(self) -> str:
        return self._class_name

    @class_name.setter
    def class_name(self, class_name: str | None) -> None:
        self._class_name = class_name or self.__class__.__name__

    @property
    def name(self) -> str:
        if self.physics_object is None:
            return self.class_name

        return f"{self.physics_object.name}.{self.class_name}"

    @property
    def value(self) -> ak.Array:
        try:
            return ak.to_regular(self._value, axis=None)

        except Exception:
            return self._value

    @value.setter
    def value(self, value: ak.Array | None) -> None:
        self._value = value or ak.Array([])

    @property
    def config(self) -> dict:
        return {
            "physics_object": str(self.physics_object),
            "class_name": self.class_name,
        }

    def read(self, events) -> "Observable":
        if self.physics_object is None:
            raise ValueError("No physics object specified")

        all_branches = {key.lower(): key for key in events.keys(recursive=False)}
        all_keys = {key.lower(): key for key in events.keys(full_paths=False)}

        branch = self.physics_object.branch.lower()
        slices = self.physics_object.slices
        observable = self.__class__.__name__.lower()

        if f"{branch}.{observable}" in all_keys:
            key = all_keys[f"{branch}.{observable}"]
            array = events[key].array()
            value = array[:, *slices]

        elif "constituents" in branch:
            constituents = get_constituents(events, all_keys[branch])
            value = getattr(constituents, observable)[:, *slices]

        else:
            momentum4d = branches_to_momentum4d(events, all_branches[branch])
            value = getattr(momentum4d, observable)[:, *slices]
            print(str(value.type))

        for i, slice_ in enumerate(slices):
            if slice_.stop is not None:
                start = slice_.start if slice_.start is not None else 0
                required_length = slice_.stop - start

                if i + 1 == len(slices):
                    value = ak.pad_none(value, required_length, axis=i + 1)
                    nan_float32 = np.array([np.nan], dtype="float32")[0]
                    value = ak.fill_none(value, nan_float32)

                else:
                    n_missing = required_length - ak.num(value, i + 1)
                    pad = ak.unflatten(ak.Array([[]] * ak.sum(n_missing)), n_missing)
                    value = ak.concatenate([value, pad], axis=i + 1)

        self._value = value

        return self
