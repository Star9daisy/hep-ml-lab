from __future__ import annotations

from typing import Any

from .physics_object import PhysicsObject


def is_single(identifier: str | PhysicsObject) -> bool:
    """Check if an identifier or an instance corresponds to a single physics object.

    Parameters
    ----------
    identifier : str | PhysicsObject
        A unique string for a physics object or an instance of a physics object.

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
    if isinstance(identifier, PhysicsObject):
        return isinstance(identifier, Single)

    try:
        Single.from_id(identifier)
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

    def __init__(self, field: str, index: int):
        self.field = field
        self.index = index
        self.objects = []

    def read_ttree(self, ttree: Any) -> Single:
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

        ! If the index is out of range, the objects will be empty:
        >>> Single("Jet", 100).read(event).objects
        []
        """
        self.objects = []

        if ttree is None:
            return self

        object = getattr(ttree, self.field, None)
        if object is None:
            raise ValueError(
                f"Could not fetch {self.field} in the entry {type(ttree)}\n"
                "Use `dir(entry)` to check all the available attributes."
            )

        if self.index < object.GetEntries():
            self.objects.append(object[self.index])

        return self

    @property
    def id(self) -> str:
        """The unique string for a single physics object.

        It consists of the name and the index.

        Examples
        --------
        >>> Single("Jet", 0).identifier
        Jet0
        """
        return f"{self.field}{self.index}"

    @classmethod
    def from_id(cls, id: str) -> Single:
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
        if "," in id:
            raise ValueError(
                "Invalid identifier for Single. The comma',' indicates it "
                "corresponds to a multiple physics object.\n"
                f"Use `Multiple.from_identifier('{id}')` instead."
            )

        if "." in id:
            raise ValueError(
                "Invalid identifier for Single. The period'.' indicates it "
                "corresponds to a nested physics object.\n"
                f"Use `Nested.from_identifier('{id}')` instead."
            )

        if ":" in id:
            raise ValueError(
                "Invalid identifier for Single. The colon':' indicates it "
                "corresponds to a collective physics object.\n"
                f"Use `Collective.from_identifier('{id}')` instead."
            )

        number = "".join(filter(lambda x: x.isdigit(), id))
        name = id.replace(number, "")
        index = int(number)

        return cls(name, index)

    @property
    def config(self) -> dict[str, Any]:
        """The configurations for serialization"""
        return {
            "classname": self.__class__.__name__,
            "field": self.field,
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

        return cls(config["field"], config["index"])
