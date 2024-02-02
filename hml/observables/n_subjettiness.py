from __future__ import annotations

from math import nan

from ..physics_objects.single import is_single
from .observable import Observable


class NSubjettiness(Observable):
    def __init__(self, physics_object: str, n: int):
        self.n = n
        supported_types = ["single", "collective"]

        super().__init__(physics_object, supported_types)

    def read_ttree(self, event):
        objs = self.physics_object.read_ttree(event).objects

        if is_single(self.physics_object.name):
            self._value = objs[0].Tau[self.n - 1] if objs != [] else nan

        else:
            self._value = [
                obj.Tau[self.n - 1] if obj is not None else nan for obj in objs
            ]

        return self

    @property
    def config(self):
        config = super().config
        config.update({"n": self.n})
        return config


class TauN(NSubjettiness):
    @property
    def name(self):
        return f"{self.physics_object.name}.Tau{self.n}"

    @classmethod
    def from_name(cls, name: str, **kwargs) -> TauN:
        if "." not in name:
            raise ValueError(f"Invalid name {name}.")

        physics_object, class_name = name.split(".")
        n = int(class_name[-1])

        return cls(physics_object, n, **kwargs)


NSubjettiness.add_alias("n_subjettiness")
TauN.add_alias("tau_n")
