from __future__ import annotations

import awkward as ak

from ..operations import branch_to_momentum4d, constituents_to_momentum4d
from ..physics_objects import PhysicsObject, is_collective, is_multiple, is_single
from ..physics_objects import parse_physics_object as parse_object


class Observable:
    aliases = {}

    def __init__(
        self,
        physics_object: str | PhysicsObject | None = None,
        class_name: str | None = None,
        supported_objects: list[str | PhysicsObject] | None = None,
    ) -> None:
        self._physics_object = self._init_object(physics_object)
        self._class_name = self._init_class_name(class_name)
        self._supported_objects = self._init_supported_objects(supported_objects)
        self._validate_physics_object()

    def __init_subclass__(cls, **kwargs):
        cls.aliases[cls.__name__] = cls

    @classmethod
    def with_aliases(cls, *aliases: str) -> Observable:
        for alias in aliases:
            cls.aliases[alias] = cls

    def _init_object(self, object_: str | PhysicsObject | None) -> PhysicsObject | None:
        if isinstance(object_, PhysicsObject):
            return object_

        elif isinstance(object_, str):
            return parse_object(object_)

        else:
            return

    def _init_class_name(self, class_name: str | None) -> str:
        return class_name if class_name else self.__class__.__name__

    def _init_supported_objects(
        self, supported_objects: list[str | PhysicsObject] | None
    ) -> list[PhysicsObject] | None:
        if supported_objects is None:
            return

        output = []
        for obj in supported_objects:
            if isinstance(obj, PhysicsObject):
                output.append(obj.__class__.__name__.lower())
            else:
                output.append(obj.lower())

        return output

    def _validate_physics_object(self) -> None:
        if self.supported_objects is None:
            return

        elif self.physics_object is None and self.supported_objects is not None:
            raise ValueError

        elif "multiple" not in self.supported_objects:
            if (
                self.physics_object.__class__.__name__.lower()
                not in self.supported_objects
            ):
                raise ValueError

        else:
            if not is_multiple(self.physics_object, self.supported_objects):
                raise ValueError

    def __eq__(self, other: str | Observable) -> bool:
        if isinstance(other, str):
            other = self.from_name(other)

        return (
            self.physics_object == other.physics_object
            and self.__class__ == other.__class__
        )

    def __repr__(self) -> str:
        return f"{self.name}: {self.value.type!s}"

    @property
    def physics_object(self) -> PhysicsObject | None:
        return self._physics_object

    @property
    def class_name(self) -> str:
        return self._class_name

    @property
    def supported_objects(self) -> list[str] | None:
        return self._supported_objects

    @property
    def value(self) -> ak.Array:
        if not hasattr(self, "_value"):
            self._value = ak.Array([])

        try:
            return ak.to_regular(self._value, axis=None)
        except Exception:
            return self._value

    @property
    def name(self) -> str:
        if self.physics_object:
            return f"{self.physics_object.name}.{self.class_name}"
        else:
            return self.class_name

    @property
    def config(self) -> dict:
        return {
            "physics_object": self.physics_object.name if self.physics_object else None,
            "class_name": self.class_name,
        }

    def read(self, events) -> Observable:
        if "multiple" in self.supported_objects:
            raise NotImplementedError

        all_keys = {i.lower(): i for i in events.keys(full_paths=False)}
        branch = self.physics_object.branch.lower()
        slices = self.physics_object.slices

        if branch is None:
            raise ValueError(f"Branch {self.physics_object.branch} not found")

        if is_single(self.physics_object) or is_collective(self.physics_object):
            if f"{branch}.{self.__class__.__name__.lower()}" in all_keys:
                key = all_keys[f"{branch}.{self.__class__.__name__.lower()}"]
                value = events[key].array()

            else:
                array = branch_to_momentum4d(events, all_keys[branch])
                value = getattr(array, self.__class__.__name__.lower())

        else:
            array = constituents_to_momentum4d(events, all_keys[branch])
            value = getattr(array, self.__class__.__name__.lower())

        if len(slices) == 1:
            value = value[:, slices[0]]
        else:
            value = value[:, slices[0], slices[1]]

        for i, slice_ in enumerate(slices):
            if slice_.stop is not None:
                start = slice_.start if slice_.start is not None else 0
                required_length = slice_.stop - start

                if i + 1 == len(slices) and ak.any(
                    ak.num(value, i + 1) < required_length
                ):
                    value = ak.pad_none(value, required_length, axis=i + 1)

                else:
                    n_missing = required_length - ak.num(value, i + 1)
                    if ak.sum(n_missing) > 0:
                        pad = ak.unflatten(
                            ak.Array([[]] * ak.sum(n_missing)), n_missing
                        )
                        value = ak.concatenate([value, pad], axis=i + 1)

        self._value = value

        return self

    @classmethod
    def from_name(cls, name: str, **kwargs) -> "Observable":
        *parts, class_name = name.split(".")
        physics_object = ".".join(parts) if len(parts) > 0 else None

        if "class_name" in kwargs:
            class_name = kwargs["class_name"]
            del kwargs["class_name"]

        return cls(physics_object=physics_object, class_name=class_name, **kwargs)

    @classmethod
    def from_config(cls, config: dict) -> "Observable":
        return cls(**config)

    @property
    def shape(self) -> str:
        *parts, _ = str(self.value.type).split(" * ")
        return tuple(parts)

    @property
    def dtype(self) -> type:
        *_, dtype = str(self.value.type).split(" * ")
        return dtype
