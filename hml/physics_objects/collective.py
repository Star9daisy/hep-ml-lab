from __future__ import annotations

from typing import Any

from .physics_object import PhysicsObject
from .single import Single


def is_collective(identifier: str) -> bool:
    """Checks if an identifier can be used to create a collective physics object.

    Parameters
    ----------
    identifier : str
        A string that represents a collective physics object.

    Returns
    -------
    result : bool

    Examples
    --------
    >>> is_collective("Jet:")
    True

    >>> is_collective("Jet0") # Single
    False

    >>> is_collective("Jet0.Particles:100") # Nested
    False

    >>> is_collective("Jet0,Jet1") # Multiple
    False
    """
    try:
        Collective.from_identifier(identifier)
        return True

    except Exception:
        return False


class Collective(PhysicsObject):
    """A collective physics object.

    It represents a collection of physics objects in an event or a branch. For
    example, the leading three jets, all the constituents of the leading jet, etc.

    This class works like proxy of a real object. After reading a source, use
    `objects` to show the corresponding objects.

    Parameters
    ----------
    name : str
        The name of the physics object.
    start : int
        The starting index of the physics object.
    stop : int
        The stopping index of the physics object.

    Examples
    --------
    Create a collective physics object by its name, starting and stopping indices:
    >>> obj = Collective("Jet", 1, 2)
    >>> obj
    'Jet1:2'

    The stopping index is optional. If not given, it will read all objects:
    >>> obj = Collective("Jet", 1)
    >>> obj
    'Jet1:'

    So is the starting index. If not given, it will start from the first object:
    >>> obj = Collective("Jet", stop=2)
    >>> obj
    'Jet:2'

    Default indices mean all objects:
    >>> obj = Collective("Jet")
    >>> obj
    'Jet:'

    The identifier of a collective physics object is composed of its name and
    indices:
    >>> obj = Collective("Jet", 1, 2)
    >>> obj.identifier
    'Jet1:2'

    Also, you can create a collective physics object from its identifier:
    >>> obj = Collective.from_identifier("Jet0:2")
    >>> obj == Collective("Jet", 0, 2)
    True
    """

    def __init__(self, name: str, start: int = 0, stop: int = -1):
        self.name = name
        self.start = start
        self.stop = stop
        self.objects = []

    def read(self, source: Any):
        """Read a collective physics object from an event or a branch.

        Each time it reads a source, it will refresh the `objects` list. The
        `objects` are a list of elements.

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
        Read an event to fetch the leading three jets:
        >>> obj = Collective("Jet", 0, 3)
        >>> obj.read(event)
        >>> obj.objects
        [<cppyy.gbl.Jet object at 0x8ec8850>,
        <cppyy.gbl.Jet object at 0x8ec8e80>,
        <cppyy.gbl.Jet object at 0x8ec94b0>]

        Or read the jet branch to fetch all the constituents of the leading jet:
        >>> obj = Collective("Particles")
        >>> obj.read(event.Jet[0])
        >>> len(obj.objects)
        21

        It supports method chaining:
        >>> len(Collective("Jet", 0, 3).read(event).objects)
        3

        If the starting index is out of range, an empty list will be returned:
        >>> Collective("Jet", 100).read(event).objects
        []

        If the stopping index is out of range, `None` will be filled to ensure
        the length of the objects:
        >>> Collective("Jet", 3, 6).read(event).objects
        [<cppyy.gbl.Jet object at 0x920a1f0>,
        <cppyy.gbl.Jet object at 0x920a820>,
        None]
        """
        self.objects = []
        object = getattr(source, self.name, None)

        if object is None:
            raise ValueError(
                f"Could not find object {self.name} in such type {type(source)}"
            )

        if self.stop == -1:
            self.objects = [
                Single(self.name, i).read(source).objects[0]
                for i in range(self.start, object.GetEntries())
            ]
        else:
            self.objects = [
                Single(self.name, i).read(source).objects[0]
                for i in range(self.start, self.stop)
            ]

        return self

    @property
    def identifier(self) -> str:
        """The identifier of the collective physics object.

        It is the name followed by the slice-like indices, e.g. Jet:, Jet1:,
        Jet:2, Jet1:2, etc.
        """
        if self.start == 0 and self.stop == -1:
            return f"{self.name}:"

        elif self.start == 0:
            return f"{self.name}:{self.stop}"

        elif self.stop == -1:
            return f"{self.name}{self.start}:"

        else:
            return f"{self.name}{self.start}:{self.stop}"

    @classmethod
    def from_identifier(cls, identifier):
        """Create a collective physics object from an identifier.

        It will break down the identifier to get the name and indices for the
        physics object.

        Parameters
        ----------
        identifier : str
            The identifier of a collective physics object.

        Returns
        -------
        physics object : Collective
            The collective physics object.

        Raises
        ------
        ValueError
            If there's no colon`:` or there's any comma`,` or period`.` in the identifier.
        """
        if ":" not in identifier:
            raise ValueError(
                "Invalid identifier for Collective. The colon':' is missing.\n"
                "Correct the identifier like 'Jet:'."
            )

        if "," in identifier:
            raise ValueError(
                "Invalid identifier for Collective. The comma',' indicates it "
                "corresponds to a multiple physics object.\n"
                f"Use `Multiple.from_identifier('{identifier}')` instead."
            )

        if "." in identifier:
            raise ValueError(
                "Invalid identifier for Collective. The period'.' indicates it "
                "corresponds to a nested physics object.\n"
                f"Use `Nested.from_identifier('{identifier}')` instead."
            )

        first, second = identifier.split(":")
        start = "".join(filter(lambda x: x.isdigit(), first))
        name = first.replace(start, "")
        start = int(start) if start != "" else 0
        stop = int(second) if second != "" else -1

        return cls(name, start, stop)

    @property
    def config(self):
        """The configurations for serialization"""
        return {
            "classname": "Collective",
            "name": self.name,
            "start": self.start,
            "stop": self.stop,
        }

    @classmethod
    def from_config(cls, config):
        """Create a collective physics object from configurations.

        Parameters
        ----------
        config : dict
            Configurations for a collective physics object.

        Returns
        -------
        physics object : Collective
            The collective physics object.

        Raises
        ------
        ValueError
            If `classname` in the configurations is not "Collective".
        """
        if config["classname"] != "Collective":
            raise ValueError(
                f"Invalid classname {config.get('classname')}. Expected 'Collective'."
            )

        return cls(config["name"], config["start"], config["stop"])

    def __repr__(self) -> str:
        return f"{self.identifier}"

    def __eq__(self, other: Collective) -> bool:
        if (
            self.name == other.name
            and self.start == other.start
            and self.stop == other.stop
        ):
            return True

        return False
