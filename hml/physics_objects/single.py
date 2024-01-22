from __future__ import annotations

from typing import Any

from .physics_object import PhysicsObject


def is_single(identifier: str) -> bool:
    """Check if an identifier can be used to create an instance of the `Single`
    class.

    Parameters
    ----------
    identifier : str
        A string that represents a single object.

    Returns
    -------
    result : bool

    Examples
    --------
    >>> is_single("Jet0")
    True

    >>> is_single("Jet:") # Collective
    False

    >>> is_single("Jet0.Particles:100") # Nested
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

    It represents one specific object in an event or one sub-object of an object.
    For example, the leading jet, the first constituent of that jet, etc.

    This class works like proxy of a real object. After reading a source, use
    `objects` to show the corresponding object(s).

    Parameters
    ----------
    name : str
        The name of the physics object.
    index : int
        The index of the physics object.

    Examples
    --------
    Create a single physics object by its name and index:
    >>> from hml.physics_objects import Single
    >>> obj = Single("Jet", 0)
    >>> obj
    'Jet0'

    The identifier of a single object is composed of its name and index:
    >>> obj.identifier
    'Jet0'

    Also, you can create a single object from such an identifier:
    >>> obj = Single.from_identifier("Jet0")
    >>> obj == Single("Jet", 0)
    True
    """

    def __init__(self, name: str, index: int):
        self.name = name
        self.index = index
        self.objects = []

    def read(self, source: Any):
        """Read a single physics object from an event or a branch.

        Each time it reads a source, it will refresh the `objects` list. The
        `objects` are a list of only one element.

        Parameters
        ----------
        source : Any
            An event(entry) or a branch loaded by PyROOT.

        Raises
        ------
        ValueError
            If the name is not a valid branch in the event or a valid leaf of
            the branch.

        Examples
        --------
        You can use `DelphesEvents` to read events from a ROOT file:
        >>> from hml.events import DelphesEvents
        >>> events = DelphesEvents("tag_1_delphes_events.root")

        Read an event to fetch the leading jet:
        >>> obj = Single("Jet", 0)
        >>> obj.read(events[0])
        >>> obj.objects
        [<cppyy.gbl.Jet object at 0x9a7f9c0>]

        Or read the jet branch to fetch the leading particle of the leading jet:
        >>> obj = Single("Particles", 0)
        >>> obj.read(events[0].Jet[0])
        >>> obj.objects
        [<cppyy.gbl.GenParticle object at 0x7a2ee90>]

        It supports method chaining:
        >>> Single("Jet", 0).read(events[0]).objects
        [<cppyy.gbl.Jet object at 0x9a7f9c0>]
        >>> Single("Particles", 0).read(events[0].Jet[0]).objects
        [<cppyy.gbl.GenParticle object at 0x7a2ee90>]

        If the index is out of range, the object will be None:
        >>> obj = Single("Jet", 100)
        >>> obj.read(events[0])
        >>> obj.objects
        [None]
        """
        self.objects = []

        object = getattr(source, self.name, None)
        if object is None:
            raise ValueError(
                f"Could not find {self.name} in the source of type {type(source)}\n"
                "Use `dir(source)` to check all the available "
                "attributes of the source."
            )

        if self.index >= object.GetEntries():
            self.objects.append(None)
        else:
            self.objects.append(object[self.index])

        return self

    @property
    def identifier(self) -> str:
        """The identifier of the single physics object.

        It is the name followed by the index of the physics object, e.g. Jet0,
        Jet1, etc.
        """
        return f"{self.name}{self.index}"

    @classmethod
    def from_identifier(cls, identifier: str):
        """Create a single physics object from an identifier.

        It will break down the identifier to get the name and index for the
        physics object.

        Parameters
        ----------
        identifier : str
            The identifier of the single object.

        Returns
        -------
        physics object : Single
            The single physics object.

        Raises
        ------
        ValueError
            If there is any of the comma`,`, the period`.`, or the colon`:`.
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
    def config(self):
        """The configurations for serialization"""
        return {
            "classname": self.__class__.__name__,
            "name": self.name,
            "index": self.index,
        }

    @classmethod
    def from_config(cls, config: dict[str, Any]):
        """Create a single physics object from configurations.

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
