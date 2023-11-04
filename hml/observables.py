from __future__ import annotations

from abc import ABC, abstractmethod
from itertools import product
from typing import Any

import numpy as np
from ROOT import TTree  # type: ignore


def get_observable(name: str, **kwargs) -> Observable:
    """Get an observable from its name.

    An observable name is composed of two parts: the shortcut and the class name.
    For example, `Jet_0.Pt` is the name of the `Pt` observable of the first jet,
    in which `Jet_0` is the shortcut and `Pt` is the class name.
    """
    if len(parts := name.split(".")) == 1:
        shortcut, classname = "", parts[0]
    else:
        shortcut, classname = parts

    if classname not in Observable.all_observables:
        raise ValueError(f"Observable {classname} not found")

    return Observable.all_observables[classname](shortcut, **kwargs)


class Observable(ABC):
    """Base class for observables.

    Implement the `get_value` method to define a new observable.
    """

    all_observables = {}

    def __init__(
        self,
        shortcut: str | None = None,
        object_pairs: list[tuple[str, int | None]] | None = None,
    ) -> None:
        self.seprate_branch_name_and_index = "_"
        self.separate_objects = "-"

        if shortcut:
            self.shortcut = shortcut
            self.object_pairs = self.parse_shortcut(shortcut)
        elif object_pairs:
            self.shortcut = self.build_shortcut(object_pairs)
            self.object_pairs = object_pairs
        else:
            self.shortcut = None
            self.object_pairs = None

        self._value = None

    @property
    def name(self) -> str:
        """The name of the observable.

        The name is composed of the shortcut and the class name, e.g. `Jet_0.Pt`.
        """
        if self.shortcut:
            return f"{self.shortcut}.{self.__class__.__name__}"
        else:
            return self.__class__.__name__

    @property
    def value(self) -> Any:
        """The value of the observable."""
        return self._value

    def to_numpy(self) -> np.ndarray:
        """Convert the value to a numpy array."""
        return np.array(self.value, dtype=np.float32)

    def __repr__(self) -> str:
        """The representation of the observable."""
        return f"{self.name}: {self.value}"

    def read_event(self, event: TTree) -> Observable:
        """Read an event and fetch the needed physics objects.

        It creates three attributes: event, objects and _value. The _value is
        calculated by calling the `get_value` method.
        """
        self.event = event
        self.objects = []
        self._value = None

        if self.object_pairs:
            for branch_name, index in self.object_pairs:
                if branch_name in event.GetListOfBranches():
                    branch = getattr(event, branch_name)

                    if index is None:
                        self.objects.append([i for i in branch])
                    elif index < branch.GetEntries():
                        self.objects.append(branch[index])

        self._value = self.get_value()

        return self

    @abstractmethod
    def get_value(self) -> Any:
        """Calculate the value of the observable.

        Implement this method to define a new observable. Here're common cases:
        1. Quick calculation: use `self.event` to get physics objects and write
        the calculation directly.
        2. Take the advantage of Observable: use `self.objects` to do the
        calculation.

        Return None if the observable is not correctly got.
        """
        ...  # pragma: no cover

    def parse_shortcut(self, shortcut: str) -> list[tuple[str, int | None]]:
        """Parse the shortcut to get the object pairs."""
        object_pairs = []
        objects = shortcut.split(self.separate_objects)
        for obj in objects:
            if "_" in obj:
                branch_name, index = obj.split(self.seprate_branch_name_and_index)
                index = int(index)
            else:
                branch_name, index = obj, None

            object_pairs.append((branch_name, index))
        return object_pairs

    def build_shortcut(self, object_pairs: list[tuple[str, int | None]]) -> str:
        """Build the shortcut from the object pairs."""
        shortcuts = []
        for branch_name, index in object_pairs:
            if index is not None:
                obj = f"{branch_name}{self.seprate_branch_name_and_index}{index}"
            else:
                obj = branch_name
            shortcuts.append(obj)
        return self.separate_objects.join(shortcuts)

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        Observable.all_observables[cls.__name__] = cls

    @classmethod
    def add_alias(cls, *alias: str) -> None:
        """Add alias for the class name."""
        for i in alias:
            Observable.all_observables[i] = cls


class Px(Observable):
    """Get the x component of the momentum.

    Available for single and multiple objects. For example:
    - `Jet_0.Px` is the x component of the momentum of the leading jet.
    - `Jet.Px` is the x component of the momentum of all jets.

    Alias: px
    """

    def get_value(self) -> Any:
        if len(self.objects) == 0:
            return

        obj = self.objects[0]
        if isinstance(obj, list):
            return [i.P4().Px() for i in obj]
        else:
            return obj.P4().Px()


class Py(Observable):
    """Get the y component of the momentum.

    Available for single and multiple objects. For example:
    - `Jet_0.Py` is the y component of the momentum of the leading jet.
    - `Jet.Py` is the y component of the momentum of all jets.

    Alias: py
    """

    def get_value(self) -> Any:
        if len(self.objects) == 0:
            return

        obj = self.objects[0]
        if isinstance(obj, list):
            return [i.P4().Py() for i in obj]
        else:
            return obj.P4().Py()


class Pz(Observable):
    """Get the z component of the momentum.

    Available for single and multiple objects. For example:
    - `Jet_0.Pz` is the z component of the momentum of the leading jet.
    - `Jet.Pz` is the z component of the momentum of all jets.

    Alias: pz
    """

    def get_value(self) -> Any:
        if len(self.objects) == 0:
            return

        obj = self.objects[0]
        if isinstance(obj, list):
            return [i.P4().Pz() for i in obj]
        else:
            return obj.P4().Pz()


class E(Observable):
    """Get the energy of the object.

    Available for single and multiple objects. For example:
    - `Jet_0.E` is the energy of the leading jet.
    - `Jet.E` is the energy of all jets.

    Alias: e, Energy
    """

    def get_value(self) -> Any:
        if len(self.objects) == 0:
            return

        obj = self.objects[0]
        if isinstance(obj, list):
            return [i.P4().E() for i in obj]
        else:
            return obj.P4().E()


class Pt(Observable):
    """Get the transverse momentum of the object.

    Available for single and multiple objects. For example:
    - `Jet_0.Pt` is the transverse momentum of the leading jet.
    - `Jet.Pt` is the transverse momentum of all jets.

    Alias: pt, pT, PT
    """

    def get_value(self) -> Any:
        if len(self.objects) == 0:
            return

        obj = self.objects[0]
        if isinstance(obj, list):
            return [i.P4().Pt() for i in obj]
        else:
            return obj.P4().Pt()


class Eta(Observable):
    """Get the pseudorapidity of the object.

    Available for single and multiple objects. For example:
    - `Jet_0.Eta` is the pseudorapidity of the leading jet.
    - `Jet.Eta` is the pseudorapidity of all jets.

    Alias: eta
    """

    def get_value(self) -> Any:
        if len(self.objects) == 0:
            return

        obj = self.objects[0]
        if isinstance(obj, list):
            return [i.P4().Eta() for i in obj]
        else:
            return obj.P4().Eta()


class Phi(Observable):
    """Get the azimuthal angle of the object.

    Available for single and multiple objects. For example:
    - `Jet_0.Phi` is the azimuthal angle of the leading jet.
    - `Jet.Phi` is the azimuthal angle of all jets.

    Alias: phi
    """

    def get_value(self) -> Any:
        if len(self.objects) == 0:
            return

        obj = self.objects[0]
        if isinstance(obj, list):
            return [i.P4().Phi() for i in obj]
        else:
            return obj.P4().Phi()


class M(Observable):
    """Get the mass of the object.

    Available for single and multiple objects. For example:
    - `Jet_0.M` is the mass of the leading jet.
    - `Jet.M` is the mass of all jets.

    Alias: m, mass, Mass"""

    def get_value(self) -> Any:
        if len(self.objects) == 0:
            return

        obj = self.objects[0]
        if isinstance(obj, list):
            return [i.P4().M() for i in obj]
        else:
            return obj.P4().M()


class DeltaR(Observable):
    """Calculate the deltaR between two objects.

    Available for two objects. For example:
    - `Jet_0-Jet_1.DeltaR` is the deltaR between the leading two jets.
    - `Jet_0-Jet.DeltaR` is the deltaR between the leading jet and all jets.
    - `Jet-Jet.DeltaR` is the deltaR between all jets.

    """

    def get_value(self) -> Any:
        if len(self.objects) != 2:
            return

        obj1, obj2 = self.objects
        obj1 = [obj1] if not isinstance(obj1, list) else obj1
        obj2 = [obj2] if not isinstance(obj2, list) else obj2

        distances = []
        for i, j in product(obj1, obj2):
            distances.append(i.P4().DeltaR(j.P4()))

        return distances[0] if len(distances) == 1 else distances


class NSubjettiness(Observable):
    """Get the n-subjettiness from the leaf Tau of the branch FatJet.

    Available for single FatJet objects. For example:
    - `FatJet_0.NSubjettiness` is the tau1 (by default) of the leading FatJet.

    Alias: TauN
    """

    def __init__(
        self,
        shortcut: str | None = None,
        object_pairs: list[tuple[str, int | None]] | None = None,
        n: int = 1,
    ) -> None:
        super().__init__(shortcut, object_pairs)
        self.n = n

    def get_value(self) -> Any:
        if len(self.objects) == 0:
            return

        obj = self.objects[0]
        if isinstance(obj, list):
            return [i.Tau[self.n - 1] for i in obj]
        else:
            return obj.Tau[self.n - 1]


class NSubjettinessRatio(Observable):
    """Calculate the n-subjettiness ratio from the leaf Tau of the branch FatJet.

    Available for single FatJet objects. For example:
    - `FatJet_0.NSubjettinessRatio` is the tau21 (by default) of the leading
    FatJet.

    Alias: TauMN
    """

    def __init__(
        self,
        shortcut: str | None = None,
        object_pairs: list[tuple[str, int | None]] | None = None,
        m: int = 2,
        n: int = 1,
    ) -> None:
        super().__init__(shortcut, object_pairs)
        self.m = m
        self.n = n

    def get_value(self) -> Any:
        if len(self.objects) == 0:
            return

        obj = self.objects[0]
        if isinstance(obj, list):
            return [i.Tau[self.m - 1] / i.Tau[self.n - 1] for i in obj]
        else:
            return obj.Tau[self.m - 1] / obj.Tau[self.n - 1]


class Size(Observable):
    """The number of physics objects.

    Available for single object. For example:
    - `Jet.Size` is the number of jets.

    Alias: size
    """

    def get_value(self):
        if len(self.objects) > 0:
            return len(self.objects[0])


Px.add_alias("px")
Py.add_alias("py")
Pz.add_alias("pz")
E.add_alias("e", "Energy")

Pt.add_alias("pt", "pT", "PT")
Eta.add_alias("eta")
Phi.add_alias("phi")
M.add_alias("m", "mass", "Mass")

NSubjettiness.add_alias("TauN")
NSubjettinessRatio.add_alias("TauMN")

Size.add_alias("size")

Energy = E
PT = Pt
Mass = M
TauN = NSubjettiness
TauMN = NSubjettinessRatio
