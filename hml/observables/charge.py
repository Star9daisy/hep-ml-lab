from __future__ import annotations

from ..physics_objects import PhysicsObject
from .observable import Observable


class Charge(Observable):
    def __init__(
        self,
        physics_object: str | PhysicsObject,
        class_name: str | None = None,
    ) -> None:
        supported_objects = ["single", "collective"]
        super().__init__(physics_object, class_name, supported_objects)


Charge.with_aliases("charge")
