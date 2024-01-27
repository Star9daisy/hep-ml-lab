from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Any

from .collective import Collective
from .physics_object import PhysicsObject
from .single import Single
from .single import is_single


def is_nested(identifier: str | PhysicsObject) -> bool:
    """Check if an identifier corresponds to a nested physics object.

    Parameters
    ----------
    identifier : str | PhysicsObject
        A string name or a physics object instance.

    Returns
    -------
    result : bool

    Examples
    --------
    >>> is_nested("Jet0.Constituents:")
    True

    >>> main = Single(branch="Jet", index=0)
    >>> sub = Collective(branch="Constituents", start=0, stop=3)
    >>> obj = Nested(main=main, sub=sub)
    >>> is_nested(obj)
    >>> True
    """
    if isinstance(identifier, PhysicsObject):
        return isinstance(identifier, Nested)

    try:
        Nested.from_name(identifier)
        return True

    except Exception:
        return False


@dataclass
class Nested(PhysicsObject):
    """The data class that represents a nested physics object.

    For example, the constituents of the leading jet, the first 100 constituents
    of the first three leading jets, etc.

    Parameters
    ----------
    main : Single | Collective
        The main physics object.
    sub : Single | Collective
        The sub physics object.

    Attributes
    ----------
    name : str
        The name of the physics object.
    value : list[Any] | None
        The fetched values of the physics objects.

    Examples
    --------
    Create a nested physics object by its main and sub physics objects:
    >>> main = Single(branch="Jet", index=0)
    >>> sub = Collective(branch="Constituents", start=3, stop=6)
    >>> Nested(main=main, sub=sub)
    Nested(name='Jet0.Constituents3:6', value=None)

    Create a nested physics object from its name:
    >>> Nested.from_name("Jet0.Constituents3:6")
    Nested(name='Jet0.Constituents3:6', value=None)

    Read an event to fetch the first three constituents of the leading jet:
    >>> main = Single(branch="Jet", index=0)
    >>> sub = Collective(branch="Constituents", stop=3)
    >>> obj = Nested(main=main, sub=sub).read_ttree(event)
    >>> obj
    Nested(name='Jet0.Constituents:3', value=[[<cppyy.gbl.Tower object at 0x9683af0>, <cppyy.gbl.Track object at 0x9041bd0>, <cppyy.gbl.Track object at 0x9041f90>]])

    Use `main` and `sub` to show details:
    >>> obj.main
    Single(name='Jet0', value=<cppyy.gbl.Jet object at 0xa08dab0>)
    >>> obj.sub
    Collective(name='Constituents:3', value=[<cppyy.gbl.Tower object at 0x9683af0>, <cppyy.gbl.Track object at 0x9041bd0>, <cppyy.gbl.Track object at 0x9041f90>])
    """

    main: Single | Collective = field(repr=False)
    sub: Single | Collective = field(repr=False)
    name: str = field(init=False, compare=False)
    value: list[Any] | None = field(default=None, init=False, compare=False)

    def __post_init__(self):
        self.name = f"{self.main.name}.{self.sub.name}"

    def read_ttree(self, event: Any) -> Nested:
        """Read an event to fetch the value.

        Parameters
        ----------
        event : TTree
            An event read by PyROOT.

        Returns
        -------
        self : Nested

        Examples
        --------
        Read an event to fetch the first ten constituents of the first two
        leading jet:
        >>> main = Collective(branch="Jet", stop=2)
        >>> sub = Collective(branch="Constituents", stop=10)
        >>> obj = Nested(main=main, sub=sub).read_ttree(event)
        Collective(name='Constituents:10', value=[<cppyy.gbl.Tower object at 0x9683790>, <cppyy.gbl.Track object at 0x9041090>, <cppyy.gbl.Tower object at 0x9683940>, <cppyy.gbl.Track object at 0x8514610>, <cppyy.gbl.Track object at 0x9040af0>, <cppyy.gbl.Track object at 0x9040280>, <cppyy.gbl.Tower object at 0x9835b20>, <cppyy.gbl.Track object at 0x9040cd0>, <cppyy.gbl.Track object at 0x9040910>, <cppyy.gbl.Track object at 0x9040be0>])

        The lengths of objects keep nested:

        - Single + Single -> 1, 1
        >>> obj = Nested.from_name("Jet0.Constituents0").read_ttree(event)
        >>> len(obj.value), len(obj.value[0])
        (1, 1)
        >>> obj.value
        [[<cppyy.gbl.Tower object at 0x9683af0>]]

        - Single + Collective -> 1, var (depending on the stop index)
        >>> obj = Nested.from_name("Jet0.Constituents:4").read_ttree(event)
        >>> len(obj.value), len(obj.value[0])
        (1, 4)
        >>> obj.value
        [[<cppyy.gbl.Tower object at 0x9683af0>,
         <cppyy.gbl.Track object at 0x9041bd0>,
         <cppyy.gbl.Track object at 0x9041f90>,
         <cppyy.gbl.Tower object at 0x9683c10>]]

        >>> obj = Nested.from_name("Jet0.Constituents:").read_ttree(event)
        >>> len(obj.value), len(obj.value[0])
        (1, 21)
        >>> obj.value
        [[<cppyy.gbl.Tower object at 0x9683af0>,
          <cppyy.gbl.Track object at 0x9041bd0>,
          <cppyy.gbl.Track object at 0x9041f90>,
          <cppyy.gbl.Tower object at 0x9683c10>,
          <cppyy.gbl.Track object at 0x90419f0>,
          <cppyy.gbl.Track object at 0x9040eb0>,
          <cppyy.gbl.Track object at 0x9041ea0>,
          <cppyy.gbl.Track object at 0x9041db0>,
          <cppyy.gbl.Track object at 0x9040fa0>,
          <cppyy.gbl.Track object at 0x9041900>,
          <cppyy.gbl.Tower object at 0x9683b80>,
          <cppyy.gbl.Track object at 0x9041810>,
          <cppyy.gbl.Track object at 0x9040dc0>,
          <cppyy.gbl.Tower object at 0x9835bb0>,
          <cppyy.gbl.Track object at 0x9041630>,
          <cppyy.gbl.Tower object at 0x9683a60>,
          <cppyy.gbl.Track object at 0x9041270>,
          <cppyy.gbl.Track object at 0x9041450>,
          <cppyy.gbl.Track object at 0x9041360>,
          <cppyy.gbl.Track object at 0x9041ae0>,
          <cppyy.gbl.Tower object at 0x96839d0>]]

        Here is a table for all possible cases of fetched value:

        |                 | Jet0       | Jet100     | Jet:100      | Jet100: |
        |-----------------|------------|------------|--------------|---------|
        | Constituent0    | o (1, 1)   | x (1, 1)   | ? (100, 1)   | x []    |
        | Constituent100  | x (1, 1)   | x (1, 1)   | x (100, 1)   | x []    |
        | Constituent:100 | ? (1, 100) | x (1, 100) | ? (100, 100) | x []    |
        | Constituent100: | x (1, 0)   | x (1, 0)   | x (100, 0)   | x []    |

        - First row: the main physics object
        - Second row: the sub physics object
        - "o": correct
        - "x": incorrect
        - "?": some of the objects are `None`

        """
        self.value = []

        self.main.read_ttree(event)
        main_values = (
            [self.main.value] if isinstance(self.main, Single) else self.main.value
        )

        for obj in main_values:
            self.sub.read_ttree(obj)
            sub_values = (
                [self.sub.value] if isinstance(self.sub, Single) else self.sub.value
            )
            self.value.append(sub_values)

        return self

    @classmethod
    def from_name(cls, name: str) -> Nested:
        """Create a nested physics object from its name.

        Parameters
        ----------
        name: str

        Returns
        -------
        physics object : Nested

        Raises
        ------
        ValueError
            If the name is invalid.
        """
        main_name, sub_name = name.split(".")
        main = (
            Single.from_name(main_name)
            if is_single(main_name)
            else Collective.from_name(main_name)
        )
        sub = (
            Single.from_name(sub_name)
            if is_single(sub_name)
            else Collective.from_name(sub_name)
        )

        return cls(main, sub)
