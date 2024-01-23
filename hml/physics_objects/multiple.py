from __future__ import annotations

from typing import Any

from .collective import Collective
from .collective import is_collective
from .nested import Nested
from .nested import is_nested
from .physics_object import PhysicsObject
from .single import Single
from .single import is_single


def is_multiple(
    identifier: str,
    supported_types: list[str] | None = None,
) -> bool:
    """Check if an identifier corresponds to a multiple physics object.

    Parameters
    ----------
    identifier : str
        A unique string for a physics object.
    supported_types : list[str], optional
        The supported types of physics objects it contains. Valid values are
        "single", "collective", and "nested". If None, all types are supported.

    Returns
    -------
    result : bool

    Examples
    --------
    By default, all types are supported for each physics object:
    >>> is_multiple("Jet0,Jet1")
    True

    >>> is_multiple("Jet0") # Single
    False

    >>> is_multiple("Jet:") # Collective
    False

    >>> is_multiple("Jet0.Constituents:") # Nested
    False

    Specify the supported types to check strictly:
    >>> is_multiple("Jet0,Jet1", ["single"])
    True

    >>> is_multiple("Jet0,Jet1", ["collective"])
    False

    >>> is_multiple("Jet0,Jet1", ["nested"])
    False
    """
    try:
        obj = Multiple.from_identifier(identifier)

    except Exception:
        return False

    if supported_types is None:
        return True

    supported_classes = []
    for classname in supported_types:
        if classname.lower() == "single":
            supported_classes.append(Single)
        elif classname.lower() == "collective":
            supported_classes.append(Collective)
        elif classname.lower() == "nested":
            supported_classes.append(Nested)
        else:
            raise ValueError(
                f"Invalid supported type {classname}. "
                f"Valid values are 'single', 'collective', and 'nested'."
            )

    for i in obj.all:
        if type(i) not in supported_classes:
            return False

    return True


class Multiple(PhysicsObject):
    """A multiple physics object.

    It represents multiple physics objects in combination of single, collective,
    and nested physics objects. For example, three leading jets, all jets and all
    electrons, constituents of the leading jet and sub-leading jet, etc.

    Parameters
    ----------
    *physics_objects : Single | Collective | Nested
        The physics objects.

    Examples
    --------
    Create a multiple physics object by its physics objects:
    >>> obj = Multiple(Single("Jet", 0), Single("Jet", 1))
    >>> obj
    Jet0,Jet1
    >>> obj.all
    (Jet0, Jet1)

    >>> obj = Multiple(Collective("Jet"), Collective("Electron"))
    >>> obj
    Jet:,Electron:
    >>> obj.all
    (Jet:, Electron:)

    It is represented by the identifier:
    >>> obj = Multiple(Single("Jet", 0), Single("Jet", 1))
    >>> obj
    Jet0,Jet1
    >>> obj.identifier
    Jet0,Jet1

    Create a multiple physics object from an identifier:
    >>> Multiple.from_identifier("Jet0,Jet1")
    Jet0,Jet1
    """

    def __init__(self, *physics_objects: Single | Collective | Nested):
        self.all = physics_objects
        self.objects = []

    def read(self, entry: Any) -> Multiple:
        """Read an entry to fetch the objects.

        Since a multiple physics object may contain nested ones, the entry is
        expected to be an event.

        Parameters
        ----------
        entry : Any
            An event read by PyROOT.

        Returns
        -------
        self : Multiple

        Examples
        --------
        Read an event to fetch the leading three jets:
        >>> obj = Multiple.from_identifier("Jet0,Jet1,Jet2").read(event)
        >>> obj.objects
        [[<cppyy.gbl.Jet object at 0x7eb6ed0>],
        [<cppyy.gbl.Jet object at 0x7eb7500>],
        [<cppyy.gbl.Jet object at 0x7eb7b30>]]

        Use `all` to show details:
        >>> obj.all
        (Jet0, Jet1, Jet2)
        >>> obj.all[0].objects
        [<cppyy.gbl.Jet object at 0x7eb6ed0>]

        ! For any failure cases, check the doc for `Single.read`, `Collective.read`,
        and `Nested.read`.
        """
        self.objects = [obj.read(entry).objects for obj in self.all]
        return self

    @property
    def identifier(self) -> str:
        """The unique string for a multiple physics object.

        It consists of the identifiers of all physics objects it contains, and a
        comma is used to separate them.
        """
        return ",".join([obj.identifier for obj in self.all])

    @classmethod
    def from_identifier(cls, identifier: str) -> Multiple:
        """Create a multiple physics object from an identifier.

        It decomposes the identifier into identifiers that may correspond to
        single, collective, or nested physics objects.

        Parameters
        ----------
        identifier : str
            A unique string for a physics object.

        Returns
        -------
        physics object : Multiple

        Raises
        ------
        ValueError
            No comma`,` or invalid identifier.
        """
        if "," not in identifier:
            raise ValueError(f"Invalid identifier {identifier} for {cls.__name__}")

        objects = []
        for i in identifier.split(","):
            if is_single(i):
                objects.append(Single.from_identifier(i))
            elif is_collective(i):
                objects.append(Collective.from_identifier(i))
            elif is_nested(i):
                objects.append(Nested.from_identifier(i))
            else:
                raise ValueError(f"Invalid identifier {identifier} for {cls.__name__}")
        return cls(*objects)

    @property
    def config(self) -> dict[str, Any]:
        """The configurations for serialization."""
        return {
            "classname": "Multiple",
            "configs": [obj.config for obj in self.all],
        }

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> Multiple:
        """Create a multiple physics object from configurations.

        Parameters
        ----------
        config : dict

        Returns
        -------
        physics object : Multiple

        Raises
        ------
        ValueError
            If `classname` in the configurations is not "Multiple".
        """
        if config.get("classname") != "Multiple":
            raise ValueError(f"Invalid config for {cls.__name__}")

        objects = []
        for obj in config.get("configs"):
            if obj.get("classname") == "Single":
                objects.append(Single.from_config(obj))
            elif obj.get("classname") == "Collective":
                objects.append(Collective.from_config(obj))
            elif obj.get("classname") == "Nested":
                objects.append(Nested.from_config(obj))
            else:
                raise ValueError(f"Invalid config for {cls.__name__}")
        return cls(*objects)

    def __repr__(self) -> str:
        return self.identifier

    def __eq__(self, other: Multiple) -> bool:
        for obj1, obj2 in zip(self.all, other.all):
            if obj1 != obj2:
                return False
        return True
