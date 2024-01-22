from __future__ import annotations

from typing import Any

from .physics_object import PhysicsObject
from .single import Single


def is_collective(identifier: str) -> bool:
    """Checks if an identifier can be used to create a collective object.

    Parameters
    ----------
    identifier : str
        A unique string that represents a physics object.

    """
    try:
        Collective.from_identifier(identifier)
        return True
    except Exception:
        return False


class Collective(PhysicsObject):
    """A collective physics object.

    It represents a collection of physics objects in an event or a branch. For example, the leading three jets or all the constituents of the leading jet.

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
    Create a collective object by its name and starting and stopping indices:
    >>> from hml.physics_objects import Collective
    >>> obj = Collective("Jet", 1, 2)
    >>> obj
    'Jet1:2'

    The stopping index is optional:
    >>> obj = Collective("Jet", 1)
    >>> obj
    'Jet1:'

    So is the starting index:
    >>> obj = Collective("Jet", stop=2)
    >>> obj
    'Jet:2'

    Default indices mean all objects:
    >>> obj = Collective("Jet")
    >>> obj
    'Jet:'

    Create a collective object from its identifier:
    >>> obj = Collective.from_identifier("Jet0:2")
    >>> obj == Collective("Jet", 0, 2)
    True
    """

    def __init__(self, name, start=0, stop=-1):
        self.name = name
        self.start = start
        self.stop = stop
        self.objects = []

    def read(self, source: Any):
        """Read a collective object from an event or a branch.

        Parameters
        ----------
        source : Any
            An event(entry) or a branch read by PyROOT.

        Raises
        ------
        ValueError
            If the name is not a valid branch in the event or a valid leaf of
            the branch.

        Examples
        --------
        >>> from hml.events import DelphesEvents
        >>> from hml.physics_objects import Collective
        >>> events = DelphesEvents("tag_1_delphes_events.root")

        Read an event to fetch the leading three jets:
        >>> obj = Collective("Jet", 0, 3)
        >>> obj.read(events[0])
        >>> obj.objects
        [<cppyy.gbl.Jet object at 0x8ec8850>,
        <cppyy.gbl.Jet object at 0x8ec8e80>,
        <cppyy.gbl.Jet object at 0x8ec94b0>]

        Or read the jet branch to fetch all the constituents of the leading jet:
        >>> obj = Collective("Particles")
        >>> obj.read(events[0].Jet[0])
        >>> len(obj.objects)
        21

        If the starting index is out of range, an empty list will be returned:
        >>> obj = Collective("Jet", 100)
        >>> obj.read(events[0])
        >>> obj.objects
        []

        If the stopping index is out of range, `None` will be filled to ensure
        the length of the objects:
        >>> obj = Collective("Jet", 3, 6)
        >>> obj.read(events[0])
        >>> obj.objects
        [<cppyy.gbl.Jet object at 0x920a1f0>,
        <cppyy.gbl.Jet object at 0x920a820>,
        None]
        """
        # Reset the object list every time we read a new event
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
        """The identifier of the collective object.

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
        """Create a collective object from an identifier.

        It will parse the identifier to get the name and slice-like indices of
        the object.

        Parameters
        ----------
        identifier : str
            The identifier of the collective object.

        Returns
        -------
        object : Collective
            The collective object.

        Raises
        ------
        ValueError
            When there's any of the comma`,`, the perioid`.`.
        """
        if "," in identifier:
            raise ValueError(
                "Invalid identifier.\n"
                "',' in the identifier indicates this is a multiple physics object.\n"
                f"Use `Multiple.from_identifier('{identifier}')` instead."
            )

        if "." in identifier:
            raise ValueError(
                "Invalid identifier.\n"
                "'.' in the identifier indicates this is a nested physics object.\n"
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
        """Configurations of a collective object."""
        return {
            "classname": "Collective",
            "name": self.name,
            "start": self.start,
            "stop": self.stop,
        }

    @classmethod
    def from_config(cls, config):
        """Create a collective object from configurations.

        Parameters
        ----------
        config : dict
            Configurations of a collective object.

        Returns
        -------
        object : Collective
            The collective object.

        Raises
        ------
        ValueError
            When the classname is not "Collective".
        """
        if config["classname"] != "Collective":
            raise ValueError(
                "Invalid classname.\n"
                f"Expected 'Collective', got '{config['classname']}'."
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
