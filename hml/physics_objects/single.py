from __future__ import annotations

from typing import Any

from .physics_object import PhysicsObject


def is_single(identifier: str) -> bool:
    """Check if an identifier corresponds to a single physics object.

    Parameters
    ----------
    identifier : str
        A unique string for a physics object.

    Returns
    -------
    result : bool

    Examples
    --------
    >>> is_single("Jet0")
    True

    >>> is_single("Jet:") # Collective
    False

    >>> is_single("Jet0.Constituents:100") # Nested
    False

    >>> is_single("Jet0,Jet1") # Multiple
    False
    """
    try:
        Single.from_identifier(identifier)
        return True

    except Exception:
        return False


class Single(PhysicsObject):
    """A single physics object.

    It represents one specific object, e.g. the leading jet, the first constituent
    of the leading jet, etc.

    Parameters
    ----------
    name : str
        The name of the physics object.
    index : int
        The index of the physics object.

    Examples
    --------
    Create a single physics object by its name and index:
    >>> obj = Single("Jet", 0)
    >>> obj.name, obj.index
    ('Jet', 0)

    It is represented by the identifier:
    >>> obj = Single("Jet", 0)
    >>> obj
    Jet0
    >>> obj.identifier
    Jet0

    Create a single physics object from an identifier:
    >>> Single.from_identifier("Jet0")
    Jet0
    """

    def __init__(self, name: str, index: int):
        self.name = name
        self.index = index
        self.objects = []

    def read(self, entry: Any) -> Single:
        """Read an entry to fetch the objects.

        Every time it is called, the objects will be cleared and re-filled.

        Parameters
        ----------
        entry : Any
            An event or a branch read by PyROOT.

        Returns
        -------
        self : Single

        Raises
        ------
        ValueError
            If the name is not a valid attribute of the entry.

        Examples
        --------
        Read an event to fetch the leading jet:
        >>> Single("Jet", 0).read(event).objects
        [<cppyy.gbl.Jet object at 0x9a7f9c0>]

        Read the leading jet to fetch the first constituent:
        >>> Single("Constituents", 0).read(event.Jet[0]).objects
        [<cppyy.gbl.Tower object at 0x8f59ed0>]

        ! If the index is out of range, the object will be None:
        >>> Single("Jet", 100).read(event).objects
        [None]
        """
        self.objects = []

        object = getattr(entry, self.name, None)
        if object is None:
            raise ValueError(
                f"Could not fetch {self.name} in the entry {type(entry)}\n"
                "Use `dir(entry)` to check all the available attributes."
            )

        if self.index >= object.GetEntries():
            self.objects.append(None)
        else:
            self.objects.append(object[self.index])

        return self

    @property
    def identifier(self) -> str:
        """The unique string for a single physics object.

        It consists of the name and the index.

        Examples
        --------
        >>> Single("Jet", 0).identifier
        Jet0
        """
        return f"{self.name}{self.index}"

    @classmethod
    def from_identifier(cls, identifier: str) -> Single:
        """Create a single physics object from an identifier.

        It decomposes the identifier into a name and an index to construct a
        single physics object.

        Parameters
        ----------
        identifier : str
            A unique string for a physics object.

        Returns
        -------
        physics object : Single

        Raises
        ------
        ValueError
            If there's any of the comma`,`, the period`.`, or the colon`:`.
        """
        if "," in identifier:
            raise ValueError(
                "Invalid identifier for Single. The comma',' indicates it "
                "corresponds to a multiple physics object.\n"
                f"Use `Multiple.from_identifier('{identifier}')` instead."
            )

        if "." in identifier:
            raise ValueError(
                "Invalid identifier for Single. The period'.' indicates it "
                "corresponds to a nested physics object.\n"
                f"Use `Nested.from_identifier('{identifier}')` instead."
            )

        if ":" in identifier:
            raise ValueError(
                "Invalid identifier for Single. The colon':' indicates it "
                "corresponds to a collective physics object.\n"
                f"Use `Collective.from_identifier('{identifier}')` instead."
            )

        number = "".join(filter(lambda x: x.isdigit(), identifier))
        name = identifier.replace(number, "")
        index = int(number)

        return cls(name, index)

    @property
    def config(self) -> dict[str, Any]:
        """The configurations for serialization"""
        return {
            "classname": self.__class__.__name__,
            "name": self.name,
            "index": self.index,
        }

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> Single:
        """Create a single physics object from configurations.

        Parameters
        ----------
        config : dict

        Returns
        -------
        physics object : Single

        Raises
        ------
        ValueError
            If `classname` in the configurations is not "Single".

        """
        if config.get("classname") != "Single":
            raise ValueError(
                f"Invalid classname {config.get('classname')}. Expected 'Single'."
            )

        return cls(config["name"], config["index"])

    def __repr__(self) -> str:
        return f"{self.identifier}"

    def __eq__(self, other: Single) -> bool:
        if self.name == other.name and self.index == other.index:
            return True
        else:
            return False
