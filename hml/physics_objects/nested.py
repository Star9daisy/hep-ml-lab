from __future__ import annotations

from typing import Any

from .collective import Collective
from .physics_object import PhysicsObject
from .single import Single
from .single import is_single


def is_nested(identifier: str) -> bool:
    try:
        Nested.from_identifier(identifier)
        return True
    except Exception:
        return False


class Nested(PhysicsObject):
    def __init__(
        self,
        main_object: Single | Collective,
        sub_object: Single | Collective,
    ):
        self.main_object = main_object
        self.sub_object = sub_object
        self.objects = []

    def read(self, source: Any):
        self.objects = []

        self.main_object.read(source)
        for obj in self.main_object.objects:
            if obj is None:
                if (
                    isinstance(self.sub_object, Collective)
                    and self.sub_object.stop != -1
                ):
                    length = self.sub_object.stop - self.sub_object.start
                    self.objects.append([None] * length)
                else:
                    self.objects.append([None])
            else:
                self.objects.append(self.sub_object.read(obj).objects)

        return self

    @property
    def identifier(self) -> str:
        return f"{self.main_object.identifier}.{self.sub_object.identifier}"

    @classmethod
    def from_identifier(cls, identifier) -> Nested:
        if "." not in identifier:
            raise ValueError(
                "Invalid identifier.\n"
                "':' in the identifier indicates this is a collective physics object.\n"
                f"Use `Collective.from_identifier('{identifier}')` instead."
            )

        if "," in identifier:
            raise ValueError(
                "Invalid identifier.\n"
                "',' in the identifier indicates this is a multiple physics object.\n"
                f"Use `Multiple.from_identifier('{identifier}')` instead."
            )

        main_identifier, sub_identifier = identifier.split(".")

        main_identifier = (
            Single.from_identifier(main_identifier)
            if is_single(main_identifier)
            else Collective.from_identifier(main_identifier)
        )

        sub_identifier = (
            Single.from_identifier(sub_identifier)
            if is_single(sub_identifier)
            else Collective.from_identifier(sub_identifier)
        )

        return cls(main_identifier, sub_identifier)

    @property
    def config(self) -> dict[str, Any]:
        return {
            "classname": "Nested",
            "main_object_config": self.main_object.config,
            "sub_object_config": self.sub_object.config,
        }

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> Nested:
        if config.get("classname") != "Nested":
            raise ValueError(
                f"Invalid classname. Expected 'Nested', got {config['classname']}"
            )

        if config["main_object_config"].get("classname") == "Single":
            main_object = Single.from_config(config["main_object_config"])
        else:
            main_object = Collective.from_config(config["main_object_config"])

        if config["sub_object_config"].get("classname") == "Single":
            sub_object = Single.from_config(config["sub_object_config"])
        else:
            sub_object = Collective.from_config(config["sub_object_config"])

        return cls(main_object, sub_object)

    def __repr__(self) -> str:
        return self.identifier

    def __eq__(self, other: Nested) -> bool:
        if (
            self.main_object == other.main_object
            and self.sub_object == other.sub_object
        ):
            return True
        else:
            return False
