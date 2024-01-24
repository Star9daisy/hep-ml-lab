from __future__ import annotations

from typing import Any

from .collective import Collective
from .physics_object import PhysicsObject
from .single import Single
from .single import is_single


def is_nested(identifier: str | PhysicsObject) -> bool:
    """Check if an identifier or an instance corresponds to a nested physics object.

    Parameters
    ----------
    identifier : str | PhysicsObject
        A unique string for a physics object or an instance of a physics object.

    Returns
    -------
    result : bool

    Examples
    --------
    >>> is_nested("Jet0.Constituents:")
    True

    >>> is_nested("Jet0") # Single
    False

    >>> is_nested("Jet:") # Collective
    False

    >>> is_nested("Jet0,Jet1") # Multiple
    False
    """
    if isinstance(identifier, PhysicsObject):
        return isinstance(identifier, Nested)

    try:
        Nested.from_identifier(identifier)
        return True

    except Exception:
        return False


class Nested(PhysicsObject):
    """A nested physics object.

    It represents a nested physics objects, which is a combination of single and
    collective physics objects. For example, the constituents of the leading jet,
    the first 100 constituents of the first three leading jets, etc.

    Parameters
    ----------
    main : Single | Collective
        The main physics object.
    sub : Single | Collective
        The sub physics object.

    Examples
    --------
    Create a nested physics object by its main and sub objects:
    >>> obj = Nested(Single("Jet", 0), Collective("Constituents"))
    >>> obj.main, obj.sub
    (Jet0, Constituents:)

    It is represented by the identifier:
    >>> obj = Nested(Single("Jet", 0), Collective("Constituents"))
    >>> obj
    Jet0.Constituents:
    >>> obj.identifier
    Jet0.Constituents:

    Create a nested physics object from an identifier:
    >>> Nested.from_identifier("Jet0.Constituents:")
    Jet0.Constituents:
    """

    def __init__(
        self,
        main: Single | Collective,
        sub: Single | Collective,
    ):
        self.main = main
        self.sub = sub
        self.objects = []

    def read(self, entry: Any) -> Nested:
        """Read an entry to fetch the objects.

        Since nested physics objects are fetched by a hierarchy of main and sub
        objects, the entry is expected to be an event.

        Parameters
        ----------
        entry : Any
            An event read by PyROOT.

        Returns
        -------
        self : Nested

        Examples
        --------
        Read an event to fetch the first three constituents of the leading jet:
        >>> obj = Nested(Single("Jet", 0), Collective("Constituents", 0, 3))
        >>> obj.read(event).objects
        [[<cppyy.gbl.Tower object at 0x8f59ed0>,
        <cppyy.gbl.Track object at 0x7360700>,
        <cppyy.gbl.Track object at 0x7360430>]]

        Use `main` and `sub` to show details:
        >>> obj.main
        Jet0
        >>> obj.main.objects
        [<cppyy.gbl.Jet object at 0x7eb6ed0>]
        >>> obj.sub
        Constituents:3
        >>> obj.sub.objects
        [<cppyy.gbl.Tower object at 0x8f59ed0>,
        <cppyy.gbl.Track object at 0x7360700>,
        <cppyy.gbl.Track object at 0x7360430>]

        The lengths of objects keep nested:

        - Single + Single -> 1, 1
        >>> obj = Nested.from_identifier("Jet0.Constituents0").read(event)
        >>> len(obj.objects), len(obj.objects[0])
        (1, 1)

        ! If the index is out of range, the object fetched will be None but in
        the same shape:
        >>> obj = Nested.from_identifier("Jet100.Constituents0").read(event)
        >>> len(obj.objects), len(obj.objects[0])
        (1, 1, True)
        >>> obj.objects
        [[None]]
        >>> obj = Nested.from_identifier("Jet0.Constituents100").read(event)
        >>> len(obj.objects), len(obj.objects[0])
        (1, 1)
        >>> obj.objects
        [[None]]

        - Single + Collective -> 1, var (depending on the stopping index)
        >>> obj = Nested.from_identifier("Jet0.Constituents:").read(event)
        >>> len(obj.objects), len(obj.objects[0])
        (1, 20)
        >>> obj = Nested.from_identifier("Jet0.Constituents:10").read(event)
        >>> len(obj.objects), len(obj.objects[0])
        (1, 10)
        >>> obj = Nested.from_identifier("FatJet0.Constituents:").read(event)
        >>> len(obj.objects), len(obj.objects[0])
        (1, 28)
        >>> obj = Nested.from_identifier("FatJet0.Constituents:10").read(event)
        >>> len(obj.objects), len(obj.objects[0])
        (1, 10)

        ! If the index of the single is out of range:
        >>> obj = Nested.from_identifier("Jet100.Constituents:").read(event)
        >>> len(obj.objects), len(obj.objects[0])
        (1, 1)
        >>> obj.objects
        [[None]]

        ! If the starting index of the collective is out of range:
        >>> obj = Nested.from_identifier("Jet0.Constituents:100").read(event)
        >>> len(obj.objects), len(obj.objects[0])
        (1, 0)
        >>> obj.objects
        [[]]

        ! If the stopping index of the collective is out of range:
        >>> obj = Nested.from_identifier("Jet0.Constituents18:22").read(event)
        >>> len(obj.objects), len(obj.objects[0])
        (1, 4)
        >>> obj.objects
        [[<cppyy.gbl.Track object at 0x8580260>,
        <cppyy.gbl.Track object at 0x8580350>,
        None,
        None]]

        - Collective + Collective -> var, var (depending on the stopping indices)
        >>> obj = Nested.from_identifier("Jet:.Constituents:").read(event)
        >>> len(obj.objects), [len(x) for x in obj.objects]
        (4, [20, 18, 12, 8])
        >>> obj = Nested.from_identifier("Jet:3.Constituents:5").read(event)
        >>> len(obj.objects), [len(x) for x in obj.objects]
        (3, [5, 5, 5])

        ! If the first starting index is out of range:
        >>> obj = Nested.from_identifier("Jet5:.Constituents:").read(event)
        >>> len(obj.objects), [len(x) for x in obj.objects]
        (0, [])

        ! If the second starting index is out of range:
        >>> obj = Nested.from_identifier("Jet:.Constituents100:").read(event)
        >>> len(obj.objects), [len(x) for x in obj.objects]
        (4, [0, 0, 0, 0])

        ! If the first stopping index is out of range and no stopping index for
        the second:
        >>> obj = Nested.from_identifier("Jet:10.Constituents:").read(event)
        >>> len(obj.objects), [len(x) for x in obj.objects]
        (10, [20, 18, 12, 8, 1, 1, 1, 1, 1, 1])

        ! If the first stopping index is out of range and the second has a stopping
        index:
        >>> obj = Nested.from_identifier("Jet:10.Constituents:20").read(event)
        >>> len(obj.objects), [len(x) for x in obj.objects]
        (10, [20, 20, 20, 20, 20, 20, 20, 20, 20, 20])

        The stopping index leads to proper padding of `None` to ensure the shape
        of the objects.
        """
        self.objects = []
        self.main.read(entry)

        for obj in self.main.objects:
            self.objects.append(self.sub.read(obj).objects)

        return self

    @property
    def identifier(self) -> str:
        """The unique string for a nested physics object.

        It consists of the identifiers of the main and sub objects, and a period`.`
        is used to separate them.

        Examples
        --------
        >>> Nested(Single("Jet", 0), Collective("Constituents")).identifier
        Jet0.Constituents:
        >>> Nested(Collective("Jet"), Collective("Constituents")).identifier
        Jet:.Constituents:
        """
        return f"{self.main.identifier}.{self.sub.identifier}"

    @classmethod
    def from_identifier(cls, identifier: str) -> Nested:
        """Create a nested physics object from an identifier.

        It decomposes the identifier into the identifiers of the main and sub physics
        objects.

        Parameters
        ----------
        identifier : str
            A unique string for a physics object.

        Returns
        -------
        physics object : Nested

        Raises
        ------
        ValueError
            No period`.` or there's any comma`,`.
        """
        if "." not in identifier:
            raise ValueError(
                "Invalid identifier for Nested. The period'.' is missing.\n"
                "Modify the identifier like 'Jet0.Constituents:'."
            )

        if "," in identifier:
            raise ValueError(
                "Invalid identifier for Nested. The comma',' indicates it "
                "corresponds to a multiple physics object.\n"
                f"Use `Multiple.from_identifier('{identifier}')` instead."
            )

        main_identifier, sub_identifier = identifier.split(".")

        main_identifier = (
            Single.from_identifier(main_identifier)
            if is_single(main_identifier)
            else Collective.from_identifier(main_identifier)
        )

        sub_identifier = (
            Single.from_identifier(sub_identifier)
            if is_single(sub_identifier)
            else Collective.from_identifier(sub_identifier)
        )

        return cls(main_identifier, sub_identifier)

    @property
    def config(self) -> dict[str, Any]:
        """The configurations for serialization"""
        return {
            "classname": "Nested",
            "main_object_config": self.main.config,
            "sub_object_config": self.sub.config,
        }

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> Nested:
        """Create a nested physics object from configurations.

        Parameters
        ----------
        config : dict

        Returns
        -------
        physics object : Nested

        Raises
        ------
        ValueError
            If `classname` in the configurations is not "Nested".
        """
        if config.get("classname") != "Nested":
            raise ValueError(
                f"Invalid classname {config['classname']}. Expected 'Nested'."
            )

        if config["main_object_config"].get("classname") == "Single":
            main_object = Single.from_config(config["main_object_config"])
        else:
            main_object = Collective.from_config(config["main_object_config"])

        if config["sub_object_config"].get("classname") == "Single":
            sub_object = Single.from_config(config["sub_object_config"])
        else:
            sub_object = Collective.from_config(config["sub_object_config"])

        return cls(main_object, sub_object)

    def __repr__(self) -> str:
        return self.identifier

    def __eq__(self, other: Nested) -> bool:
        if self.main == other.main and self.sub == other.sub:
            return True
        else:
            return False
