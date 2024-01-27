from __future__ import annotations

import re
from dataclasses import dataclass
from dataclasses import field
from typing import Any

from .physics_object import PhysicsObject
from .single import Single


def is_collective(name: str) -> bool:
    """Check if a name corresponds to a collective physics object.

    Parameters
    ----------
    name : str
        The name of a physics object.

    Returns
    -------
    result : bool

    Examples
    --------
    >>> is_collective("Jet:")
    True
    """
    try:
        Collective.from_name(name)
        return True

    except Exception:
        return False


@dataclass
class Collective(PhysicsObject):
    """The data class that represents a collective physics object.

    For example, the leading three jets, all the constituents of the leading jet,
    etc.

    Parameters
    ----------
    branch : str
        The branch of the physics object.
    start : int
        The starting index of the physics object.
    stop : int
        The stopping index of the physics object.

    Attributes
    ----------
    name : str
        The name of the physics object.
    value : list[Any] | None
        The fetched values of the physics objects.

    Examples
    --------
    Create a collective physics object by its name, start and stop indices:
    >>> Collective(branch="Jet", start=1, stop=2)
    Collective(name='Jet1:3', value=None)

    Create a collective physics object from its name:
    >>> Collective.from_name("Jet:")
    Collective(name='Jet:', value=None)
    >>> Collective.from_name("Jet1:")
    Collective(name='Jet1:', value=None)
    >>> Collective.from_name("Jet:3")
    Collective(name='Jet:3', value=None)
    >>> Collective.from_name("Jet1:3")
    Collective(name='Jet1:3', value=None)

    Read an event to fetch the leading three jets:
    >>> Collective(branch="Jet", stop=3).read_ttree(event).value
    [<cppyy.gbl.Jet object at 0xa0be000>,
     <cppyy.gbl.Jet object at 0xa0be630>,
     <cppyy.gbl.Jet object at 0xa0bec60>]
    """

    branch: str = field(repr=False)
    start: int = field(default=0, repr=False)
    stop: int = field(default=-1, repr=False)
    name: str = field(init=False, compare=False)
    value: list[Any] | None = field(default=None, init=False, compare=False)

    def __post_init__(self):
        if self.start == 0 and self.stop == -1:
            self.name = f"{self.branch}:"
        elif self.start == 0:
            self.name = f"{self.branch}:{self.stop}"
        elif self.stop == -1:
            self.name = f"{self.branch}{self.start}:"
        else:
            self.name = f"{self.branch}{self.start}:{self.stop}"

    def read_ttree(self, event: Any) -> Collective:
        """Read an event to fetch the value.

        Parameters
        ----------
        event : TTree
            An event or a branch read by PyROOT.

        Returns
        -------
        self : Collective

        Examples
        --------
        Four cases:

        - Keep start and stop indices as default to fetch all objects:
        >>> obj = Collective(branch="Jet")
        >>> obj.read_ttree(event)
        >>> obj.value
        [<cppyy.gbl.Jet object at 0xa0be000>,
         <cppyy.gbl.Jet object at 0xa0be630>,
         <cppyy.gbl.Jet object at 0xa0bec60>,
         <cppyy.gbl.Jet object at 0xa0bf290>,
         <cppyy.gbl.Jet object at 0xa0bf8c0>]

        - Only set start index to fetch objects from it:
        >>> obj = Collective(branch="Jet", start=1)
        >>> obj.read_ttree(event)
        >>> obj.value
        [<cppyy.gbl.Jet object at 0xa0be630>,
         <cppyy.gbl.Jet object at 0xa0bec60>,
         <cppyy.gbl.Jet object at 0xa0bf290>,
         <cppyy.gbl.Jet object at 0xa0bf8c0>]

        - Only set stop index to fetch objects before it:
        >>> obj = Collective(branch="Jet", stop=3)
        >>> obj.read_ttree(event)
        >>> obj.value
        [<cppyy.gbl.Jet object at 0xa0be000>,
         <cppyy.gbl.Jet object at 0xa0be630>,
         <cppyy.gbl.Jet object at 0xa0bec60>]

        - Set both start and stop indices to fetch objects between them:
        >>> obj = Collective(branch="Jet", start=1, stop=3)
        >>> obj.read_ttree(event)
        >>> obj.value
        [<cppyy.gbl.Jet object at 0xa0be630>, <cppyy.gbl.Jet object at 0xa0bec60>]


        ! If the start index is out of range, an empty list will be returned:
        >>> obj = Collective(branch="Jet", start=100)
        >>> obj.read_ttree(event)
        >>> obj.value
        []

        ! If the stop index is out of range, `None` will be filled:
        >>> obj = Collective(branch="Jet", start=3, stop=6)
        >>> obj.read_ttree(event)
        >>> obj.value
        [<cppyy.gbl.Jet object at 0xa0bf290>,
         <cppyy.gbl.Jet object at 0xa0bf8c0>,
         None]
        """
        self.value = []

        branch = getattr(event, self.branch, None)
        n_entries = branch.GetEntries() if branch is not None else 0
        stop = self.stop if self.stop != -1 else n_entries

        for i in range(self.start, stop):
            single = Single(self.branch, i).read_ttree(event)
            self.value.append(single.value)

        return self

    @classmethod
    def from_name(cls, name: str) -> Collective:
        """Create a collective physics object from its name.

        Parameters
        ----------
        name : str

        Returns
        -------
        physics object : Collective

        Raises
        ------
        ValueError
            If the name is invalid.
        """

        if (match := re.match(r"^([a-zA-Z]+)(\d*):(\d*)$", name)) is None:
            raise ValueError(f"Invalid name '{name}' for {cls.__name__}")

        branch, start, stop = match.groups()
        start = int(start) if start else 0
        stop = int(stop) if stop else -1

        return cls(branch, start, stop)
