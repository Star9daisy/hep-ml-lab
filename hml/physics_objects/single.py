from __future__ import annotations

import re
from typing import Any

from ..validators import validate_type
from .physics_object import PhysicsObject


def is_single(physics_object: Any) -> bool:
    """Check if the provided object is a single physics object.

    It can be either an instance of `Single` or a string that matches the single
    object naming convention <branch><index>, e.g., 'jet0', 'muon1'.

    Parameters
    ----------
    physics_object : Any
        The object to check.

    Returns
    -------
    bool
        True if the object is a single physics object, False otherwise.

    Examples
    -------
    >>> from hml.physics_objects import is_single, Single
    >>> is_single("jet0")
    True
    >>> is_single(Single(branch="jet", index=0))
    True
    >>> is_single("jet") # It is a collective object.
    False
    """
    if isinstance(physics_object, PhysicsObject):
        return isinstance(physics_object, Single)

    if isinstance(physics_object, str):
        try:
            Single.from_name(physics_object)
        except Exception:
            return False
        return True

    return False


class Single(PhysicsObject):
    """A class to represent a single physics object.

    A single physics object is uniquely identified by its branch name and index
    in the branch. For example:

    - `'jet0'` represents the first jet in the 'jet' branch;
    - `'muon1'` represents the second muon in the 'muon' branch.

    Parameters
    ----------
    branch : str
        The branch name of the object.
    index : int
        The index of the object in the branch, starting from 0.

    Examples
    --------
    >>> from hml.physics_objects import Single

    >>> obj = Single(branch="jet", index=0)
    >>> obj.name, obj.branch, obj.index
    ('jet0', 'jet', 0)
    >>> obj.slices
    [slice(0, 1, None)]

    >>> obj = Single.from_name("muon1")
    >>> obj.name, obj.branch, obj.index
    ('muon1', 'muon', 1)
    >>> obj.slices
    [slice(1, 2, None)]
    """

    def __init__(self, branch: str, index: int) -> None:
        self.branch = branch
        self.index = index

    @property
    def branch(self) -> str:
        """Return the branch name."""
        return self._branch

    @branch.setter
    def branch(self, new_branch: str):
        validate_type(new_branch, str, "branch")
        self._branch = new_branch

    @property
    def index(self) -> int:
        """Return the index of the object in the branch."""
        return self._index

    @index.setter
    def index(self, new_index: int):
        validate_type(new_index, int, "index")
        self._index = new_index

    @property
    def slices(self) -> list[slice]:
        """Return a list containing the slice from index to index + 1."""
        return [slice(self.index, self.index + 1)]

    @property
    def name(self) -> str:
        """Return the name of the object in the format <branch><index>."""
        return f"{self.branch}{self.index}"

    @classmethod
    def from_name(cls, name: str) -> Single:
        """Create a single physics object by parsing its name.

        Parameters
        ----------
        name : str
            A string that follows the pattern <branch><index>.

        Returns
        -------
        Single
            A single physics object.

        Raises
        ------
        ValueError
            If the name does not match the expected pattern.
        """
        if match := re.match(r"^([a-zA-Z]+)(\d+)$", name):
            return cls(branch=match.group(1), index=int(match.group(2)))

        raise ValueError(
            f"Invalid name: '{name}'. It should be like <branch><index>, "
            "e.g. 'jet0', 'muon1'."
        )

    @property
    def config(self) -> dict:
        """Return a dictionary containing the branch and index."""
        return {"branch": self.branch, "index": self.index}

    @classmethod
    def from_config(cls, config: dict) -> Single:
        """Create a single physics object from a configuration dictionary.

        Parameters
        ----------
        config : dict
            A dictionary containing the branch and index.

        Returns
        -------
        Single
            A single physics object.

        Raises
        ------
        ValueError
            If the configuration is invalid.
        """
        try:
            return cls(branch=config["branch"], index=config["index"])
        except Exception:
            raise ValueError(
                f"Invalid configuration: {config}. It should contain the "
                "branch and index values."
            )
