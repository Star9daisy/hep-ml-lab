from __future__ import annotations

from typing import Any

from .physics_object import PhysicsObject


def is_single(identifier: str) -> bool:
    """Checks if an identifier can be used to create an instance of the `Single` class.

    Parameters
    ----------
    identifier : str
        The `identifier` parameter is a string that represents an identifier for a
        single object.

    Returns
    -------
    result : bool
        True if the identifier is valid for a Single object, False otherwise.

    Examples
    --------
    >>> is_single("Jet0")
    True
    >>> is_single("Jet:") # Collective
    False
    >>> is_single("Jet0.Particles") # Nested
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

    It represents a specific object in an event or a branch. For example, the
    leading jet or the first constituent of the leading jet.

    Parameters
    ----------
    name : str
        The name of the physics object.
    index : int
        The index of the physics object.

    Examples
    --------
    Create a single object by its name and index:
    >>> from hml.physics_objects import Single
    >>> obj = Single("Jet", 0)

    Every kind of physics objects has a unique identifier:
    >>> obj
    'Jet0'
    >>> obj.identifier
    'Jet0'

    Also, we can create a single object from an identifier:
    >>> obj = Single.from_identifier("Jet0")
    >>> obj == Single("Jet", 0)
    True
    """

    def __init__(self, name: str, index: int):
        self.name = name
        self.index = index
        self.objects = []

    def read(self, source: Any):
        """Read a single object from an event or a branch.

        Parameters
        ----------
        source : Any
            An event(entry) or a branch read by PyROOT.

        Raises
        ------
        ValueError
            If the name is not a valid branch in the event or a valid leaf of
            the branch

        Examples
        --------
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

        If the index is out of range, the object will be None:
        >>> obj = Single("Jet", 100)
        >>> obj.read(events[0])
        >>> obj.objects
        [None]
        """
        # Reset the object list every time we read a new event
        self.objects = []

        object = getattr(source, self.name, None)
        if object is None:
            raise ValueError(
                f"Could not find object {self.name} in such type {type(source)}"
            )

        if self.index >= object.GetEntries():
            self.objects.append(None)
        else:
            self.objects.append(object[self.index])

        return self

    @property
    def identifier(self) -> str:
        """The identifier of the single object.

        It is the name followed by the index of the object, e.g. Jet0, Jet1, etc.
        """
        return f"{self.name}{self.index}"

    @classmethod
    def from_identifier(cls, identifier: str):
        """Create a single object from an identifier.

        It will parse the identifier to get the name and index of the object.

        Parameters
        ----------
        identifier : str
            The identifier of the single object.

        Returns
        -------
        object : Single
            The single object.

        Raises
        ------
        ValueError
            When there's any of the comma`,`, the perioid`.`, or the colon`:`.
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

        if ":" in identifier:
            raise ValueError(
                "Invalid identifier.\n"
                "':' in the identifier indicates this is a collective physics object.\n"
                f"Use `Collective.from_identifier('{identifier}')` instead."
            )

        number = "".join(filter(lambda x: x.isdigit(), identifier))
        name = identifier.replace(number, "")
        index = int(number)

        return cls(name, index)

    @property
    def config(self):
        """Configurations of a single object."""
        return {
            "classname": self.__class__.__name__,
            "name": self.name,
            "index": self.index,
        }

    @classmethod
    def from_config(cls, config):
        """Create a single object from a configuration.

        Raises
        ------
        ValueError
            If `classname` in the configuration is not "Single"

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
