from __future__ import annotations

from math import nan
from typing import Any

from ..physics_objects.single import is_single
from .observable import Observable


class NSubjettiness(Observable):
    def __init__(
        self,
        n: int,
        physics_object: str,
        name: str | None = None,
        value: Any = None,
        dtype: Any = None,
    ):
        supported_types = ["single", "collective"]
        super().__init__(physics_object, supported_types, name, value, dtype)
        self.n = n

    def read(self, event):
        self.physics_object.read(event)

        if is_single(self.physics_object):
            obj = self.physics_object.objects[0]
            self._value = obj.Tau[self.n - 1] if obj else nan

        else:
            self._value = []
            for obj in self.physics_object.objects:
                if obj:
                    self._value.append(obj.Tau[self.n - 1])
                else:
                    self._value.append(nan)

        return self

    @property
    def config(self):
        config = super().config
        config.update({"n": self.n})
        return config


class TauN(NSubjettiness):
    @property
    def name(self):
        return f"Tau{self.n}"

    @classmethod
    def from_identifier(cls, identifier: str, **kwargs) -> TauN:
        if "." not in identifier:
            raise ValueError(f"Invalid identifier {identifier}.")

        physics_object, name = identifier.split(".")

        n = int(name[-1])
        kwargs["n"] = n
        kwargs["physics_object"] = physics_object
        kwargs["name"] = name

        return cls(**kwargs)


NSubjettiness.add_alias("n_subjettiness")
TauN.add_alias("tau_n")
