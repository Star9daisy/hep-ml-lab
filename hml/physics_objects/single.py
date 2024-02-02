from __future__ import annotations

import re
from typing import Any

from .physics_object import PhysicsObject


def is_single(name: str) -> bool:
    """Check if a name corresponds to a single physics object.

    Parameters
    ----------
    name : str
        The name of a physics object.

    Returns
    -------
    result : bool

    Examples
    --------
    >>> is_single("Jet0")
    True
    """
    try:
        Single.from_name(name)
        return True

    except Exception:
        return False


class Single(PhysicsObject):
    """The class that represents a single physics object.

    For example, the leading jet, the first constituent, the second electron, etc.

    Parameters
    ----------
    branch : str
        The branch name of the physics object.
    index : int
        The index of the physics object.

    Attributes
    ----------
    branch : str
        The branch name of the physics object.
    index : int
        The index of the physics object.
    name : str
        The name of the physics object.
    objects : list[Any] | None
        The fetched objects of the physics object.

    Examples
    --------
    Create a single physics object by its branch and index:
    >>> Single(branch="Jet", index=0)
    Single(name='Jet0', objects=None)

    Create a single physics object from its name:
    >>> Single.from_name("Jet0")
    Single(name='Jet0', objects=None)

    Read an event to fetch the leading jet:
    >>> Single(branch="Jet", index=0).read_ttree(event)
    Single(name='Jet0', objects=[<cppyy.gbl.Jet object at 0x81e4940>])
    """

    def __init__(self, branch: str, index: int):
        self.branch = branch
        self.index = index

        self._objects = None

    def read_ttree(self, event: Any) -> Single:
        """Read an event in `TTree` format to fetch the objects.

        Parameters
        ----------
        event : TTree
            An event or a branch read by PyROOT.

        Returns
        -------
        self : Single

        Examples
        --------
        Read an event to fetch the leading jet:
        >>> obj = Single(branch="Jet", index=0)
        >>> obj.read_ttree(event)
        >>> obj.objects
        [<cppyy.gbl.Jet object at 0x9a7f9c0>]

        Read the leading jet to fetch the first constituent:
        >>> obj = Single(branch="Constituents", index=0)
        >>> obj.read_ttree(event.Jet[0])
        >>> obj.objects
        [<cppyy.gbl.Tower object at 0x8f59ed0>]

        ! If the index is out of range, the objects will be an empty list:
        >>> obj = Single(branch="Jet", index=100)
        >>> obj.read_ttree(event)
        >>> obj.objects
        []
        """
        self._objects = []

        if not hasattr(event, self.branch):
            raise ValueError(f"Branch '{self.branch}' not found in the event")

        branch = getattr(event, self.branch)

        if self.index < branch.GetEntries():
            self._objects.append(branch[self.index])

        return self

    @property
    def name(self) -> str:
        return f"{self.branch}{self.index}"

    @property
    def objects(self) -> Any:
        return self._objects

    @property
    def config(self) -> dict[str, Any]:
        return {
            "branch": self.branch,
            "index": self.index,
        }

    @classmethod
    def from_name(cls, name: str) -> Single:
        """Create a single physics object from its name.

        Parameters
        ----------
        name : str

        Returns
        -------
        physics object : Single

        Raises
        ------
        ValueError
            If the name is invalid.
        """
        if (match := re.match(r"^([a-zA-Z]+)(\d+)$", name)) is None:
            raise ValueError(f"Invalid name '{name}' for {cls.__name__}")

        branch, index = match.groups()

        return cls(branch, int(index))
