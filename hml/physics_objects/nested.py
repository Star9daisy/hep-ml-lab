from __future__ import annotations

from typing import Any

from ..validators import validate_type
from .collective import Collective
from .physics_object import PhysicsObject
from .single import Single, is_single


def is_nested(physics_object: Any) -> bool:
    """Check if the provided object is a nested physics object.

    It can be either an instance of `Nested` or a string that matches the naming
    convention <main>.<sub>, which are single or collective physics objects, e.g.,
    'jet.constituents', 'jet0.constituents:5'.

    Parameters
    ----------
    physics_object : Any
        The object to check.

    Returns
    -------
    bool
        True if the object is a nested physics object, False otherwise.

    Examples
    --------
    >>> from hml.physics_objects import is_nested, Nested
    >>> is_nested("jet.constituents")
    True
    >>> is_nested(Nested(main="jet", sub="constituents"))
    True
    >>> is_nested("jet0") # It is a single object.
    False
    >>> is_nested("jet") # It is a collective object.
    False
    """
    if isinstance(physics_object, PhysicsObject):
        return isinstance(physics_object, Nested)

    if isinstance(physics_object, str):
        try:
            Nested.from_name(physics_object)
        except Exception:
            return False
        return True

    return False


class Nested(PhysicsObject):
    """A class to represent a nested physics object.

    A nested physics object is composed of two physics objects: a main and a sub
    object. Both can be either single or collective physics objects. For example:

    - `'jet.constituents'` represents all constituents of all jets in the 'jet'
    branch;
    - `'jet0.constituents:5'` represents the first 5 constituents of the first jet
    in the 'jet' branch.

    Parameters
    ----------
    main : PhysicsObject | str
        The main physics object.
    sub : PhysicsObject | str
        The sub physics object.

    Examples
    --------
    >>> from hml.physics_objects import Nested

    >>> obj = Nested(main="jet", sub="constituents")
    >>> obj.name, obj.main.name, obj.sub.name
    ('jet.constituents', 'jet', 'constituents')
    >>> obj.branch, obj.slices
    ('jet.constituents', [slice(None, None, None), slice(None, None, None)])

    >>> obj = Nested.from_name("jet1:5.constituents:100")
    >>> obj.name, obj.main.name, obj.sub.name
    ('jet1:5.constituents:100', 'jet1:5', 'constituents:100')
    >>> obj.branch, obj.slices
    ('jet.constituents', [slice(1, 5, None), slice(None, 100, None)])
    """

    def __init__(
        self,
        main: Single | Collective | str,
        sub: Single | Collective | str,
    ) -> None:
        self.main = main
        self.sub = sub

    @property
    def main(self) -> PhysicsObject:
        """Return the main physics object."""
        return self._main

    @main.setter
    def main(self, new_main: Single | Collective | str) -> None:
        validate_type(new_main, (Single, Collective, str), "main")

        if isinstance(new_main, PhysicsObject):
            self._main = new_main
        elif is_single(new_main):
            self._main = Single.from_name(new_main)
        else:
            self._main = Collective.from_name(new_main)

    @property
    def sub(self) -> PhysicsObject:
        """Return the sub physics object."""
        return self._sub

    @sub.setter
    def sub(self, new_sub: Single | Collective | str) -> None:
        validate_type(new_sub, (Single, Collective, str), "sub")

        if isinstance(new_sub, PhysicsObject):
            self._sub = new_sub
        elif is_single(new_sub):
            self._sub = Single.from_name(new_sub)
        else:
            self._sub = Collective.from_name(new_sub)

    @property
    def branch(self) -> str:
        """Return the branch name."""
        return f"{self.main.branch}.{self.sub.branch}"

    @property
    def slices(self) -> list[slice]:
        """Return a list containing the slices of the main and sub objects."""
        return [*self.main.slices, *self.sub.slices]

    @property
    def name(self) -> str:
        """Return the name of the object in the format <main>.<sub>."""
        return f"{self.main.name}.{self.sub.name}"

    @classmethod
    def from_name(cls, name: str) -> Nested:
        """Create a nested physics object by parsing its name.

        Parameters
        ----------
        name : str
            A string that follows the pattern <main>.<sub>.

        Returns
        -------
        Nested
            A nested physics object.

        Raises
        ------
        ValueError
            If the name does not match the expected pattern.
        """
        if "." in name:
            main, sub = name.split(".")
            return cls(main=main, sub=sub)

        raise ValueError(
            f"Invalid name: '{name}'. It should be like '<main>.<sub>', "
            f"e.g. 'jet.constituents', 'jet0.constituents:100'."
        )

    @property
    def config(self) -> dict:
        """Return a dictionary containing names of the main and sub objects."""
        return {"main": self.main.name, "sub": self.sub.name}

    @classmethod
    def from_config(cls, config: dict) -> Nested:
        """Create a nested physics object from a configuration dictionary.

        Parameters
        ----------
        config : dict
            A dictionary containing the names of the main and sub objects.

        Returns
        -------
        Nested
            A nested physics object.
        """
        try:
            return cls(main=config["main"], sub=config["sub"])
        except Exception:
            raise ValueError(
                f"Invalid configuration: {config}. It should contain the names "
                "of the main and sub objects."
            )
