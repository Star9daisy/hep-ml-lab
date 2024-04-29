from __future__ import annotations

from ..physics_objects import PhysicsObject
from .observable import Observable


class BTag(Observable):
    def __init__(
        self,
        physics_object: str | PhysicsObject,
        class_name: str | None = None,
    ) -> None:
        supported_objects = ["single", "collective"]
        super().__init__(physics_object, class_name, supported_objects)


BTag.with_aliases("b_tag")


class TauTag(Observable):
    def __init__(
        self,
        physics_object: str | PhysicsObject,
        class_name: str | None = None,
    ) -> None:
        supported_objects = ["single", "collective"]
        super().__init__(physics_object, class_name, supported_objects)


TauTag.with_aliases("tau_tag")
