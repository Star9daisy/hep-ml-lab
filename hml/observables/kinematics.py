from __future__ import annotations

from ..physics_objects import PhysicsObject
from .observable import Observable


class Px(Observable):
    def __init__(
        self,
        physics_object: str | PhysicsObject,
        class_name: str | None = None,
    ) -> None:
        supported_objects = ["single", "collective", "nested"]
        super().__init__(physics_object, class_name, supported_objects)


Px.with_aliases("MomentumX", "momentum_x", "px")


class Py(Observable):
    def __init__(
        self,
        physics_object: str | PhysicsObject,
        class_name: str | None = None,
    ) -> None:
        supported_objects = ["single", "collective", "nested"]
        super().__init__(physics_object, class_name, supported_objects)


Py.with_aliases("MomentumY", "momentum_y", "py")


class Pz(Observable):
    def __init__(
        self,
        physics_object: str | PhysicsObject,
        class_name: str | None = None,
    ) -> None:
        supported_objects = ["single", "collective", "nested"]
        super().__init__(physics_object, class_name, supported_objects)


Pz.with_aliases("MomentumZ", "momentum_z", "pz")


class E(Observable):
    def __init__(
        self,
        physics_object: str | PhysicsObject,
        class_name: str | None = None,
    ) -> None:
        supported_objects = ["single", "collective", "nested"]
        super().__init__(physics_object, class_name, supported_objects)


E.with_aliases("Energy", "energy", "e")


class Pt(Observable):
    def __init__(
        self,
        physics_object: str | PhysicsObject,
        class_name: str | None = None,
    ) -> None:
        supported_objects = ["single", "collective", "nested"]
        super().__init__(physics_object, class_name, supported_objects)


Pt.with_aliases("TransverseMomentum", "transverse_momentum", "pt", "PT", "pT")


class Eta(Observable):
    def __init__(
        self,
        physics_object: str | PhysicsObject,
        class_name: str | None = None,
    ) -> None:
        supported_objects = ["single", "collective", "nested"]
        super().__init__(physics_object, class_name, supported_objects)


Eta.with_aliases("Pseudorapidity", "pseudorapidity", "eta")


class Phi(Observable):
    def __init__(
        self,
        physics_object: str | PhysicsObject,
        class_name: str | None = None,
    ) -> None:
        supported_objects = ["single", "collective", "nested"]
        super().__init__(physics_object, class_name, supported_objects)


Phi.with_aliases("AzimuthalAngle", "azimuthal_angle", "phi")


class M(Observable):
    def __init__(
        self,
        physics_object: str | PhysicsObject,
        class_name: str | None = None,
    ) -> None:
        supported_objects = ["single", "collective", "nested"]
        super().__init__(physics_object, class_name, supported_objects)


M.with_aliases("Mass", "mass", "m")
