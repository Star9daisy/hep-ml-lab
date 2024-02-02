from __future__ import annotations

from typing import Any

from .collective import Collective
from .physics_object import PhysicsObject
from .single import Single
from .single import is_single


def is_nested(name: str) -> bool:
    """Check if a name corresponds to a nested physics object.

    Parameters
    ----------
    name : str
        The name of a physics object.

    Returns
    -------
    result : bool

    Examples
    --------
    >>> is_nested("Jet0.Constituents:")
    True
    """
    try:
        Nested.from_name(name)
        return True

    except Exception:
        return False


class Nested(PhysicsObject):
    """The class that represents a nested physics object.

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
    main : Single | Collective
        The main physics object.
    sub : Single | Collective
        The sub physics object.
    name : str
        The name of the physics object.
    objects : list[Any] | None
        The fetched objects of the physics objects.

    Examples
    --------
    Create a nested physics object by its main and sub physics objects:
    >>> main = Single(branch="Jet", index=0)
    >>> sub = Collective(branch="Constituents", start=3, stop=6)
    >>> Nested(main=main, sub=sub)
    Nested(name='Jet0.Constituents3:6', objects=None)

    Create a nested physics object from its name:
    >>> Nested.from_name("Jet0.Constituents3:6")
    Nested(name='Jet0.Constituents3:6', objects=None)

    Read an event to fetch the first three constituents of the leading jet:
    >>> main = Single(branch="Jet", index=0)
    >>> sub = Collective(branch="Constituents", stop=3)
    >>> obj = Nested(main=main, sub=sub).read_ttree(event)
    >>> obj
    Nested(name='Jet0.Constituents:3', objects=[[<cppyy.gbl.Tower object at 0x9683af0>, <cppyy.gbl.Track object at 0x9041bd0>, <cppyy.gbl.Track object at 0x9041f90>]])

    Use `main` and `sub` to show details:
    >>> obj.main
    Single(name='Jet0', objects=[<cppyy.gbl.Jet object at 0xa08dab0>])
    >>> obj.sub
    Collective(name='Constituents:3', objects=[<cppyy.gbl.Tower object at 0x9683af0>, <cppyy.gbl.Track object at 0x9041bd0>, <cppyy.gbl.Track object at 0x9041f90>])
    """

    def __init__(self, main: Single | Collective, sub: Single | Collective):
        self.main = main
        self.sub = sub

        self._objects = None

    def read_ttree(self, event: Any) -> Nested:
        """Read an event in `TTree` format to fetch the objects.

        Parameters
        ----------
        event : TTree
            An event read by PyROOT.

        Returns
        -------
        self : Nested

        Examples
        --------
        Read an event to fetch the first three constituents of the first two
        leading jet:
        >>> main = Collective(branch="Jet", stop=2)
        >>> sub = Collective(branch="Constituents", stop=3)
        >>> Nested(main=main, sub=sub).read_ttree(event)
        Nested(name='Jet:2.Constituents:3', objects=[[<cppyy.gbl.Tower object at 0x9919e00>, <cppyy.gbl.Track object at 0x92d8610>, <cppyy.gbl.Track object at 0x92d8340>], [<cppyy.gbl.Track object at 0x92d7530>, <cppyy.gbl.Track object at 0x92d7440>, <cppyy.gbl.Tower object at 0x9a84d10>]])

        The lengths of objects keep nested:
        - The `Single` objects may have a length of 1 or 0.
        - The `Collective` objects may have a length greater or equal to 0.

        When the main object fails to fetch the objects, the objects length will
        be zero: (v, v) -> (0,):
        >>> obj = Nested.from_name("Jet100.Constituents0").read_ttree(event)
        >>> len(obj.objects)
        0
        >>> obj.objects
        []

        >>> obj = Nested.from_name("Jet100:.Constituents:").read_ttree(event)
        >>> len(obj.objects)
        0
        >>> obj.objects
        []

        Otherwise the objects length is composed of the main and sub objects:

        - Single + Single -> (1, v)
        >>> obj = Nested.from_name("Jet0.Constituents100").read_ttree(event)
        >>> len(obj.objects), len(obj.objects[0])
        (1, 0)
        >>> obj.objects
        [[]]

        >>> obj = Nested.from_name("Jet0.Constituents0").read_ttree(event)
        >>> len(obj.objects), len(obj.objects[0])
        (1, 1)
        >>> obj.objects
        [[<cppyy.gbl.Tower object at 0x9683af0>]]

        - Single + Collective -> 1, v (depending on the stop index)
        >>> obj = Nested.from_name("Jet0.Constituents100:").read_ttree(event)
        >>> len(obj.objects), len(obj.objects[0])
        (1, 0)
        >>> obj.objects
        [[]]

        >>> obj = Nested.from_name("Jet0.Constituents:4").read_ttree(event)
        >>> len(obj.objects), len(obj.objects[0])
        (1, 4)
        >>> obj.objects
        [[<cppyy.gbl.Tower object at 0x9683af0>,
         <cppyy.gbl.Track object at 0x9041bd0>,
         <cppyy.gbl.Track object at 0x9041f90>,
         <cppyy.gbl.Tower object at 0x9683c10>]]

        >>> obj = Nested.from_name("Jet0.Constituents:").read_ttree(event)
        >>> len(obj.objects), len(obj.objects[0])
        (1, 21)
        >>> obj.objects
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

        Here is a summary of all possible lengths of fetched objects:

        |                  | Jet0       | Jet100 | Jet:100      | Jet100: |
        |------------------|------------|--------|--------------|---------|
        | Constituents0    | o (1, 1)   | x (0,) | ? (100, 1)   | x (0,)  |
        | Constituents100  | x (1, 0)   | x (0,) | x (100, 0)   | x (0,)  |
        | Constituents:100 | ? (1, 100) | x (0,) | ? (100, 100) | x (0,)  |
        | Constituents100: | x (1, 0)   | x (0,) | x (100, 0)   | x (0,)  |

        - First row: the main physics object
        - Second row: the sub physics object
        - "o": correct
        - "x": incorrect
        - "?": some of the objects are `None`

        """
        self._objects = []

        self.main.read_ttree(event)

        if len(self.main.objects) == 0:
            return self

        for obj in self.main.objects:
            if obj is None:
                self._objects.append([])
            else:
                self.sub.read_ttree(obj)
                self._objects.append(self.sub.objects)

        return self

    @property
    def name(self) -> str:
        return f"{self.main.name}.{self.sub.name}"

    @property
    def objects(self) -> Any:
        return self._objects

    @property
    def config(self) -> dict[str, Any]:
        return {
            "main": {
                "class_name": self.main.__class__.__name__,
                "config": self.main.config,
            },
            "sub": {
                "class_name": self.sub.__class__.__name__,
                "config": self.sub.config,
            },
        }

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

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> Nested:
        class_dict = {
            "Single": Single,
            "Collective": Collective,
        }

        main_cls = class_dict[config["main"]["class_name"]]
        main = main_cls.from_config(config["main"]["config"])

        sub_cls = class_dict[config["sub"]["class_name"]]
        sub = sub_cls.from_config(config["sub"]["config"])

        return cls(main, sub)
