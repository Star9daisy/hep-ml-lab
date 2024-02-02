from __future__ import annotations

from math import nan
from typing import Any

from ..physics_objects.single import is_single
from .observable import Observable


class NSubjettinessRatio(Observable):
    def __init__(self, physics_object: str, m: int, n: int):
        self.m = m
        self.n = n
        supported_types = ["single", "collective"]

        super().__init__(physics_object, supported_types)

    def read_ttree(self, event) -> Any:
        objs = self.physics_object.read_ttree(event).objects

        if is_single(self.physics_object.name):
            tau_m = objs[0].Tau[self.m - 1] if objs != [] else nan
            tau_n = objs[0].Tau[self.n - 1] if objs != [] else nan
            self._value = tau_m / tau_n

        else:
            tau_m = [obj.Tau[self.m - 1] if obj is not None else nan for obj in objs]
            tau_n = [obj.Tau[self.n - 1] if obj is not None else nan for obj in objs]
            self._value = [i / j for i, j in zip(tau_m, tau_n)]

        return self

    @property
    def config(self):
        config = super().config
        config.update({"m": self.m, "n": self.n})
        return config


class TauMN(NSubjettinessRatio):
    @property
    def name(self):
        return f"{self.physics_object.name}.Tau{self.m}{self.n}"

    @classmethod
    def from_name(cls, name: str, **kwargs) -> TauMN:
        if "." not in name:
            raise ValueError(f"Invalid identifier {name}.")

        physics_object, name = name.split(".")
        m = int(name[-2])
        n = int(name[-1])

        return cls(physics_object, m, n, **kwargs)


NSubjettinessRatio.add_alias("n_subjettiness_ratio")
TauMN.add_alias("tau_mn")
