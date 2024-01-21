from math import isnan
from math import nan
from typing import Any

from ..physics_objects.physics_object import PhysicsObjectOptions
from ..physics_objects.single import is_single_physics_object
from .n_subjettiness import NSubjettiness
from .observable import Observable


class NSubjettinessRatio(Observable):
    def __init__(
        self,
        m: int,
        n: int,
        physics_object: str,
        name: str | None = None,
        supported_objects: list[PhysicsObjectOptions] = ["single", "collective"],
    ):
        super().__init__(physics_object, name, supported_objects)
        self.m = m
        self.n = n

        self.tau_m = NSubjettiness(m, physics_object)
        self.tau_n = NSubjettiness(n, physics_object)

    def read(self, event) -> Any:
        self.tau_m.read(event)
        self.tau_n.read(event)

        if is_single_physics_object(self.physics_object):
            if isnan(self.tau_m.value) or isnan(self.tau_n.value):
                self._value = nan
            else:
                self._value = self.tau_m.value / self.tau_n.value
        else:
            self._value = [
                m / n if not isnan(m) and not isnan(n) else nan
                for m, n in zip(self.tau_m.value, self.tau_n.value)
            ]

        return self

    @property
    def config(self):
        config = super().config
        config.update({"m": self.m, "n": self.n})
        return config


class TauMN(NSubjettinessRatio):
    @property
    def name(self):
        return f"Tau{self.m}{self.n}"

    @classmethod
    def from_name(cls, name: str) -> Observable:
        if "." in name:
            physics_object, name = name.split(".")
        else:
            physics_object = None

        m = int(name[-2])
        n = int(name[-1])

        return cls(m, n, physics_object, name)


NSubjettinessRatio.add_alias("n_subjettiness_ratio")
TauMN.add_alias("tau_mn")
