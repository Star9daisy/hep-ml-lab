from __future__ import annotations

from ..physics_objects import PhysicsObject
from .observable import Observable


class Size(Observable):
    def __init__(
        self,
        physics_object: str | PhysicsObject,
        class_name: str | None = None,
    ) -> None:
        supported_objects = ["collective"]
        super().__init__(physics_object, class_name, supported_objects)

    def read(self, events) -> Observable:
        all_keys = {i.lower(): i for i in events.keys(full_paths=False)}
        branch = self.physics_object.branch.lower()

        if f"{branch}_size" in all_keys:
            key = all_keys[f"{branch}_size"]
            value = events[key].array()
        else:
            raise KeyError(f"Key {branch}_size not found in the events.")

        self._value = value

        return self


Size.with_aliases("size")
