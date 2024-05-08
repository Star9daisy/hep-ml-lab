from __future__ import annotations

import re
from typing import Any

from ..validators import validate_type
from .physics_object import PhysicsObject


def is_collective(physics_object: Any) -> bool:
    """Check if the provided object is a collective physics object.

    It can be either an instance of `Collective` or a string that matches the
    naming convention <branch><?start>?:<?stop>, e.g., 'jet', 'jet0:', 'jet:10',
    'jet0:10'.

    Parameters
    ----------
    physics_object : Any
        The object to check.

    Returns
    -------
    bool
        True if the object is a collective physics object, False otherwise.

    Examples
    --------
    >>> from hml.physics_objects import is_collective, Collective
    >>> is_collective("jet")
    True
    >>> is_collective(Collective(branch="jet"))
    True
    >>> is_collective("jet0") # It is a single object.
    False
    """
    if isinstance(physics_object, PhysicsObject):
        return isinstance(physics_object, Collective)

    if isinstance(physics_object, str):
        try:
            Collective.from_name(physics_object)
        except Exception:
            return False
        return True

    return False


class Collective(PhysicsObject):
    """A class to represent a collective physics object.

    A collective physics object is identified by its branch name and an optional
    start and stop index in the branch. For example:

    - `'jet'` or `'jet:'` represents all the jets in the 'jet' branch;
    - `'jet1:'` represents all the jets starting from the second jet in the 'jet'
    branch;
    - `'jet:10'` represents all the jets up to the tenth jet in the 'jet' branch.

    Parameters
    ----------
    branch : str
        The branch name of the object.
    start : int, optional
        The start index of the object in the branch, starting from 0.
    stop : int, optional
        The stop index of the object in the branch.

    Examples
    --------
    >>> from hml.physics_objects import Collective

    >>> obj = Collective(branch="jet")
    >>> obj.name, obj.branch, obj.start, obj.stop
    ('jet', 'jet', None, None)
    >>> obj.slices
    [slice(None, None, None)]

    >>> obj = Collective.from_name("jet")
    >>> obj.name, obj.branch, obj.start, obj.stop
    ('jet', 'jet', None, None)
    >>> obj.slices
    [slice(None, None, None)]

    >>> obj = Collective.from_name("jet1:10")
    >>> obj.name, obj.branch, obj.start, obj.stop
    ('jet1:10', 'jet', 1, 10)
    >>> obj.slices
    [slice(1, 10, None)]
    """

    def __init__(
        self, branch: str, start: int | None = None, stop: int | None = None
    ) -> None:
        self.branch = branch
        self.start = start
        self.stop = stop

    @property
    def branch(self) -> str:
        """Return the branch name."""
        return self._branch

    @branch.setter
    def branch(self, new_branch: str) -> None:
        validate_type(new_branch, str, "branch")
        self._branch = new_branch

    @property
    def start(self) -> int | None:
        "Return the start index of the object in the branch."
        return self._start

    @start.setter
    def start(self, new_start: int | None) -> None:
        validate_type(new_start, (int, type(None)), "start")
        self._start = new_start

    @property
    def stop(self) -> int | None:
        """Return the stop index of the object in the branch."""
        return self._stop

    @stop.setter
    def stop(self, new_stop: int | None) -> None:
        validate_type(new_stop, (int, type(None)), "stop")
        self._stop = new_stop

    @property
    def slices(self) -> list[slice]:
        """Return a list containing the slice from start to stop."""
        return [slice(self.start, self.stop)]

    @property
    def name(self) -> str:
        """Return the name of the object in the format <branch><?start>?:<?stop>."""
        if self.start is None and self.stop is None:
            return f"{self.branch}"
        elif self.start is None:
            return f"{self.branch}:{self.stop}"
        elif self.stop is None:
            return f"{self.branch}{self.start}:"
        else:
            return f"{self.branch}{self.start}:{self.stop}"

    @classmethod
    def from_name(cls, name: str) -> Collective:
        """Create a collective physics object by parsing its name.

        Parameters
        ----------
        name : str
            A string that follows the pattern <branch><?start>?:<?stop>.

        Returns
        -------
        Collective
            A collective physics object.

        Raises
        ------
        ValueError
            If the name does not match the expected pattern.
        """
        if re.match(r"^[a-zA-Z]+$|^[a-zA-Z]+\d*:\d*$", name.strip()):
            match_ = re.match(r"^([a-zA-Z]+)(\d*):?(\d*)$", name)
            branch, start, stop = match_.groups()
            start = int(start) if start != "" else None
            stop = int(stop) if stop != "" else None

            return cls(branch=branch, start=start, stop=stop)

        raise ValueError(
            f"Invalid name: '{name}'. It should be like <branch><?start>?:<?stop>, "
            f"e.g. 'jet', 'jet1:', 'jet:5', 'jet1:5'."
        )

    @property
    def config(self) -> dict:
        """Return a dictionary containing the branch, start, and stop values."""
        return {"branch": self.branch, "start": self.start, "stop": self.stop}

    @classmethod
    def from_config(cls, config: dict) -> Collective:
        """Create a collective physics object from a configuration dictionary.

        Parameters
        ----------
        config : dict
            A dictionary containing the branch, start, and stop values.

        Returns
        -------
        Collective
            A collective physics object.

        Raises
        ------
        ValueError
            If the configuration is invalid.
        """
        try:
            return cls(
                branch=config["branch"], start=config["start"], stop=config["stop"]
            )
        except Exception:
            raise ValueError(
                f"Invalid configuration: {config}. It should contain the branch, "
                "start, and stop values."
            )
