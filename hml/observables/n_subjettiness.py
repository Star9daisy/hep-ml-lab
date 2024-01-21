from math import nan

from ..physics_objects.physics_object import PhysicsObjectOptions
from ..physics_objects.single import is_single_physics_object
from .observable import Observable


class NSubjettiness(Observable):
    def __init__(
        self,
        n: int,
        physics_object: str,
        name: str | None = None,
        supported_objects: list[PhysicsObjectOptions] = ["single", "collective"],
    ):
        super().__init__(physics_object, name, supported_objects)
        self.n = n

    def read(self, event):
        if (branch := self.physics_object.read(event)) is None:
            self._value = nan

        elif is_single_physics_object(self.physics_object):
            self._value = branch.Tau[self.n - 1]

        else:
            self._value = [
                obj.Tau[self.n - 1] if obj is not None else nan for obj in branch
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
        return f"Tau{self.n}"

    @classmethod
    def from_name(cls, name: str) -> Observable:
        if "." in name:
            physics_object, name = name.split(".")
        else:
            physics_object = None

        n = int(name[-1])

        return cls(n, physics_object, name)


NSubjettiness.add_alias("n_subjettiness")
TauN.add_alias("tau_n")
