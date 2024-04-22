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


class Py(Observable):
    def __init__(
        self,
        physics_object: str | PhysicsObject,
        class_name: str | None = None,
    ) -> None:
        supported_objects = ["single", "collective", "nested"]
        super().__init__(physics_object, class_name, supported_objects)


class Pz(Observable):
    def __init__(
        self,
        physics_object: str | PhysicsObject,
        class_name: str | None = None,
    ) -> None:
        supported_objects = ["single", "collective", "nested"]
        super().__init__(physics_object, class_name, supported_objects)


class E(Observable):
    def __init__(
        self,
        physics_object: str | PhysicsObject,
        class_name: str | None = None,
    ) -> None:
        supported_objects = ["single", "collective", "nested"]
        super().__init__(physics_object, class_name, supported_objects)


class Pt(Observable):
    def __init__(
        self,
        physics_object: str | PhysicsObject,
        class_name: str | None = None,
    ) -> None:
        supported_objects = ["single", "collective", "nested"]
        super().__init__(physics_object, class_name, supported_objects)


class Eta(Observable):
    def __init__(
        self,
        physics_object: str | PhysicsObject,
        class_name: str | None = None,
    ) -> None:
        supported_objects = ["single", "collective", "nested"]
        super().__init__(physics_object, class_name, supported_objects)


class Phi(Observable):
    def __init__(
        self,
        physics_object: str | PhysicsObject,
        class_name: str | None = None,
    ) -> None:
        supported_objects = ["single", "collective", "nested"]
        super().__init__(physics_object, class_name, supported_objects)


class M(Observable):
    def __init__(
        self,
        physics_object: str | PhysicsObject,
        class_name: str | None = None,
    ) -> None:
        supported_objects = ["single", "collective", "nested"]
        super().__init__(physics_object, class_name, supported_objects)
