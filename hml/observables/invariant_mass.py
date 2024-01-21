from typing import Any

from ROOT import TLorentzVector

from ..physics_objects.physics_object import PhysicsObjectOptions
from .observable import Observable


class InvariantMass(Observable):
    def __init__(
        self,
        physics_object: str,
        name: str | None = None,
        supported_objects: list[PhysicsObjectOptions] = ["single", "multiple"],
        dtype: Any = None,
    ):
        super().__init__(physics_object, name, supported_objects, dtype)

    def read(self, event):
        branch = self.physics_object.read(event)
        vectors = TLorentzVector()
        for obj in branch:
            if obj is not None:
                vectors += obj.P4()
            else:
                vectors += TLorentzVector()

        self._value = vectors.M()

        return self


class InvMass(InvariantMass):
    ...


class InvM(InvariantMass):
    ...


InvariantMass.add_alias("invariant_mass")
InvMass.add_alias("inv_mass")
InvM.add_alias("inv_m")
