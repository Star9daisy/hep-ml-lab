from __future__ import annotations

from typing import Any

from .collective import Collective
from .physics_object import PhysicsObject
from .single import Single
from .single import is_single


def is_nested(identifier: str) -> bool:
    """Checks if an identifier can be used to create a nested physics object.

    Parameters
    ----------
    identifier : str
        A string that represents a nested physics object.

    Returns
    -------
    result : bool

    Examples
    --------
    >>> is_nested("Jet0.Particles:")
    True

    >>> is_nested("Jet0") # Single
    False

    >>> is_nested("Jet:") # Collective
    False

    >>> is_nested("Jet0,Jet1") # Multiple
    False
    """
    try:
        Nested.from_identifier(identifier)
        return True

    except Exception:
        return False


class Nested(PhysicsObject):
    """A nested physics object.

    It represents a nested collection of physics objects in an event or a branch.
    It has main and sub objects. For example, all the constituents of the
    leading jet, the first 100 constituents of the first three leading jets, etc.

    This class works like proxy of a real object. Before reading a source, use
    `main` and `sub` to show the object proxies that will be used. After calling
    `read(event)`, use `objects` to show the corresponding objects.

    Parameters
    ----------
    main : Single | Collective
        The main physics object.
    sub : Single | Collective
        The sub physics object.

    Examples
    --------
    Create a nested physics object by its main and sub objects:
    >>> obj = Nested(Single("Jet", 0), Collective("Particles"))
    >>> obj
    'Jet0.Particles:'

    The identifier of a nested physics object is the combination of identifiers
    from the main and sub objects:
    >>> obj = Nested(Single("Jet", 0), Collective("Particles"))
    >>> obj.identifier
    'Jet0.Particles:'

    Also, you can create a nested physics object by its identifier:
    >>> obj = Nested.from_identifier("Jet0.Particles:")
    >>> obj == Nested(Single("Jet", 0), Collective("Particles"))
    True
    """

    def __init__(
        self,
        main: Single | Collective,
        sub: Single | Collective,
    ):
        self.main = main
        self.sub = sub
        self.objects = []

    def read(self, source: Any):
        self.objects = []
        self.main.read(source)

        for obj in self.main.objects:
            if obj is None:
                if isinstance(self.sub, Collective) and self.sub.stop != -1:
                    length = self.sub.stop - self.sub.start
                    self.objects.append([None] * length)
                else:
                    self.objects.append([None])
            else:
                self.objects.append(self.sub.read(obj).objects)

        return self

    @property
    def identifier(self) -> str:
        """The identifier of the nested physics object.

        It is the combination of identifiers from the main and sub objects, e.g.
        Jet0.Constituents, Jet:3.Constituents:100, etc.
        """
        return f"{self.main.identifier}.{self.sub.identifier}"

    @classmethod
    def from_identifier(cls, identifier) -> Nested:
        """Create a nested physics object from an identifier.

        It will break down the identifier to get the main and sub objects.

        Parameters
        ----------
        identifier : str
            The identifier of a nested physics object.

        Returns
        -------
        physics object : Nested
            The nested physics object.

        Raises
        ------
        ValueError
            If there's no period`.` or there's any comma`,` in the identifier.
        """
        if "." not in identifier:
            raise ValueError(
                "Invalid identifier for Nested. The period'.' is missing.\n"
                "Modify the identifier like 'Jet0.Constituents:'."
            )

        if "," in identifier:
            raise ValueError(
                "Invalid identifier for Nested. The comma',' indicates it "
                "corresponds to a multiple physics object.\n"
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
        """The configurations for serialization"""
        return {
            "classname": "Nested",
            "main_object_config": self.main.config,
            "sub_object_config": self.sub.config,
        }

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> Nested:
        """Create a nested physics object from configurations.

        Parameters
        ----------
        config : dict
            The configurations for a nested physics object.

        Returns
        -------
        physics object : Nested
            The nested physics object.

        Raises
        ------
        ValueError
            If `classname` in the configurations is not `Nested`.
        """
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
        if self.main == other.main and self.sub == other.sub:
            return True
        else:
            return False
