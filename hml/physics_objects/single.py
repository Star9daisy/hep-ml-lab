from __future__ import annotations

import re
from dataclasses import dataclass
from dataclasses import field
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


@dataclass
class Single(PhysicsObject):
    """The data class that represents a single physics object.

    For example, the leading jet, the first constituent, the second electron, etc.

    Parameters
    ----------
    branch : str
        The branch of the physics object.
    index : int
        The index of the physics object.

    Attributes
    ----------
    name : str
        The unique string for a single physics object.
    value : Any
        The fetched value of the single physics object.

    Examples
    --------
    Create a single physics object by its branch and index:
    >>> Single(branch="Jet", index=0)
    Single(name='Jet0', value=None)

    Create a single physics object from its name:
    >>> Single.from_name("Jet0")
    Single(name='Jet0', value=None)

    Read an event to fetch the leading jet:
    >>> Single(branch="Jet", index=0).read_ttree(event)
    Single(name='Jet0', value=<cppyy.gbl.Jet object at 0x81e4940>)
    """

    branch: str = field(repr=False)
    index: int = field(repr=False)
    name: str = field(init=False, compare=False)
    value: Any = field(default=None, init=False, compare=False)

    def __post_init__(self) -> None:
        self.name = f"{self.branch}{self.index}"

    def read_ttree(self, event: Any) -> Single:
        """Read an event of TTree to fetch the value.

        Parameters
        ----------
        entry : TTree
            An event or a branch read by PyROOT.

        Returns
        -------
        self : Single

        Examples
        --------
        Read an event to fetch the leading jet:
        >>> obj = Single(branch="Jet", index=0)
        >>> obj.read_ttree(event)
        >>> obj.value
        <cppyy.gbl.Jet object at 0x9a7f9c0>

        Read the leading jet to fetch the first constituent:
        >>> obj = Single(branch="Constituents", index=0)
        >>> obj.read_ttree(event.Jet[0])
        >>> obj.value
        <cppyy.gbl.Tower object at 0x8f59ed0>

        ! If the index is out of range, the value will be `None`:
        >>> obj = Single(branch="Jet", index=100)
        >>> obj.read_ttree(event)
        >>> print(obj.value)
        None
        """
        self.value = None

        if hasattr(event, self.branch):
            branch = getattr(event, self.branch)

            if self.index < branch.GetEntries():
                self.value = branch[self.index]

        return self

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
