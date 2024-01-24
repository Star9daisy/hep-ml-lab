from typing import Any

import awkward as ak
import numpy as np

from .azimuthal_angle import Phi
from .observable import Observable
from .pseudo_rapidity import Eta


class AngularDistance(Observable):
    def __init__(
        self,
        physics_object: str,
        name: str | None = None,
        value: Any = None,
        dtype: Any = None,
    ):
        supported_objects = ["single", "collective", "nested", "multiple"]
        super().__init__(physics_object, supported_objects, name, value, dtype)
        if len(self.physics_object.all) != 2:
            raise ValueError(
                "AngularDistance requires exactly two physics objects, but got"
                f" {len(self.physics_object.all)}"
            )

    def read(self, event):
        eta1 = Eta(self.physics_object.all[0].identifier).read(event)
        eta2 = Eta(self.physics_object.all[1].identifier).read(event)
        phi1 = Phi(self.physics_object.all[0].identifier).read(event)
        phi2 = Phi(self.physics_object.all[1].identifier).read(event)

        eta1_values = eta1.to_awkward()
        eta1_values = ak.flatten(eta1_values, axis=None)

        eta2_values = eta2.to_awkward()
        eta2_values = ak.flatten(eta2_values, axis=None)

        phi1_values = phi1.to_awkward()
        phi1_values = ak.flatten(phi1_values, axis=None)

        phi2_values = phi2.to_awkward()
        phi2_values = ak.flatten(phi2_values, axis=None)

        point1 = list(zip(eta1_values, phi1_values))
        point2 = list(zip(eta2_values, phi2_values))

        self._value = [
            [np.hypot(x1 - x2, y1 - y2) for x2, y2 in point2] for x1, y1 in point1
        ]

        return self


class DeltaR(AngularDistance):
    ...


AngularDistance.add_alias("angular_distance")
DeltaR.add_alias("delta_r")
