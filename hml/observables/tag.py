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


class TauTag(Observable):
    def __init__(
        self,
        physics_object: str | PhysicsObject,
        class_name: str | None = None,
    ) -> None:
        supported_objects = ["single", "collective"]
        super().__init__(physics_object, class_name, supported_objects)