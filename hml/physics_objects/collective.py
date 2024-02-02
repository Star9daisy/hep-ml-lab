from __future__ import annotations

import re
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


class Collective(PhysicsObject):
    """The class that represents a collective physics object.

    For example, the leading three jets, all the constituents of the leading jet,
    etc.

    Parameters
    ----------
    branch : str
        The branch name of the physics object.
    start : int
        The starting index of the physics object.
    stop : int
        The stopping index of the physics object.

    Attributes
    ----------
    branch : str
        The branch name of the physics object.
    start : int
        The starting index of the physics object.
    stop : int
        The stopping index of the physics object.
    name : str
        The name of the physics object.
    value : list[Any] | None
        The fetched values of the physics objects.

    Examples
    --------
    Create a collective physics object by its name, start and stop indices:
    >>> Collective(branch="Jet", start=1, stop=2)
    Collective(name='Jet1:3', objects=None)

    Create a collective physics object from its name:
    >>> Collective.from_name("Jet:")
    Collective(name='Jet:', objects=None)
    >>> Collective.from_name("Jet1:")
    Collective(name='Jet1:', objects=None)
    >>> Collective.from_name("Jet:3")
    Collective(name='Jet:3', objects=None)
    >>> Collective.from_name("Jet1:3")
    Collective(name='Jet1:3', objects=None)

    Read an event to fetch the leading three jets:
    >>> Collective(branch="Jet", stop=3).read_ttree(event).objects
    Collective(name='Jet:3', objects=[<cppyy.gbl.Jet object at 0xa323030>, <cppyy.gbl.Jet object at 0xa323660>, <cppyy.gbl.Jet object at 0xa323c90>])
    """

    def __init__(self, branch: str, start: int = 0, stop: int = -1):
        self.branch = branch
        self.start = start
        self.stop = stop

        self._objects = None

    def read_ttree(self, event: Any) -> Collective:
        """Read an event in `TTree` format to fetch the objects.

        Parameters
        ----------
        event : TTree
            An event or a branch read by PyROOT.

        Returns
        -------
        self : Collective

        Examples
        --------
        There are four cases of start and stop indices:

        - Keep start and stop indices as default to fetch all objects:
        >>> obj = Collective(branch="Jet")
        >>> obj.read_ttree(event)
        >>> obj.objects
        [<cppyy.gbl.Jet object at 0xa0be000>,
         <cppyy.gbl.Jet object at 0xa0be630>,
         <cppyy.gbl.Jet object at 0xa0bec60>,
         <cppyy.gbl.Jet object at 0xa0bf290>,
         <cppyy.gbl.Jet object at 0xa0bf8c0>]

        - Only set start index to fetch objects from it:
        >>> obj = Collective(branch="Jet", start=1)
        >>> obj.read_ttree(event)
        >>> obj.objects
        [<cppyy.gbl.Jet object at 0xa0be630>,
         <cppyy.gbl.Jet object at 0xa0bec60>,
         <cppyy.gbl.Jet object at 0xa0bf290>,
         <cppyy.gbl.Jet object at 0xa0bf8c0>]

        - Only set stop index to fetch objects before it:
        >>> obj = Collective(branch="Jet", stop=3)
        >>> obj.read_ttree(event)
        >>> obj.objects
        [<cppyy.gbl.Jet object at 0xa0be000>,
         <cppyy.gbl.Jet object at 0xa0be630>,
         <cppyy.gbl.Jet object at 0xa0bec60>]

        - Set both start and stop indices to fetch objects between them:
        >>> obj = Collective(branch="Jet", start=1, stop=3)
        >>> obj.read_ttree(event)
        >>> obj.objects
        [<cppyy.gbl.Jet object at 0xa0be630>, <cppyy.gbl.Jet object at 0xa0bec60>]


        ! If the start index is out of range, an empty list will be returned:
        >>> obj = Collective(branch="Jet", start=100)
        >>> obj.read_ttree(event)
        >>> obj.objects
        []

        ! If the stop index is out of range, `None` will be filled:
        >>> obj = Collective(branch="Jet", start=3, stop=6)
        >>> obj.read_ttree(event)
        >>> obj.objects
        [<cppyy.gbl.Jet object at 0xa0bf290>,
         <cppyy.gbl.Jet object at 0xa0bf8c0>,
         None]
        """
        self._objects = []

        if not hasattr(event, self.branch):
            raise ValueError(f"Branch '{self.branch}' not found in the event")

        branch = getattr(event, self.branch)
        n_entries = branch.GetEntries()
        stop = self.stop if self.stop != -1 else n_entries

        for i in range(self.start, stop):
            single = Single(self.branch, i).read_ttree(event)

            if len(single.objects) == 0:
                self._objects.append(None)
            else:
                self._objects.append(single.objects[0])

        return self

    @property
    def name(self) -> str:
        if self.start == 0 and self.stop == -1:
            return f"{self.branch}:"
        elif self.start == 0:
            return f"{self.branch}:{self.stop}"
        elif self.stop == -1:
            return f"{self.branch}{self.start}:"
        else:
            return f"{self.branch}{self.start}:{self.stop}"

    @property
    def objects(self) -> Any:
        return self._objects

    @property
    def config(self) -> dict[str, Any]:
        return {
            "branch": self.branch,
            "start": self.start,
            "stop": self.stop,
        }

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
