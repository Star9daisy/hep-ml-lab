from __future__ import annotations

import awkward as ak
import numpy as np

from hml.physics_objects.physics_object import PhysicsObject

from .kinematics import Eta, Phi
from .observable import Observable


class AngularDistance(Observable):
    def __init__(
        self,
        physics_object: str | PhysicsObject,
        class_name: str | None = None,
    ) -> None:
        supported_objects = ["single", "collective", "nested", "multiple"]
        super().__init__(physics_object, class_name, supported_objects)
        assert (
            len(self.physics_object.all) == 2
        ), "Two physics objects are required for angular distance"

    def read(self, events) -> None:
        obj0_eta = Eta(self.physics_object.all[0]).read(events).value
        obj0_phi = Phi(self.physics_object.all[0]).read(events).value

        obj1_eta = Eta(self.physics_object.all[1]).read(events).value
        obj1_phi = Phi(self.physics_object.all[1]).read(events).value

        if obj0_eta.ndim == 3:
            obj0_eta = ak.flatten(obj0_eta, axis=-1)
            obj0_phi = ak.flatten(obj0_phi, axis=-1)

        if obj1_eta.ndim == 3:
            obj1_eta = ak.flatten(obj1_eta, axis=-1)
            obj1_phi = ak.flatten(obj1_phi, axis=-1)

        delta_eta = obj0_eta[:, :, None] - obj1_eta[:, None, :]
        delta_phi = obj0_phi[:, :, None] - obj1_phi[:, None, :]
        self._value = np.sqrt(delta_eta**2 + delta_phi**2)

        return self

    @classmethod
    def from_name(cls, name: str, **kwargs) -> AngularDistance:
        *parts, class_name = name.split(".")
        physics_object = ".".join(parts) if len(parts) > 0 else None

        return cls(physics_object, class_name)


AngularDistance.with_aliases("angular_distance", "DeltaR", "delta_r")
