from __future__ import annotations

from abc import ABC, abstractmethod
from itertools import product
from typing import Any

import numpy as np
from ROOT import TTree  # type: ignore


def get_observable(name: str, **kwargs) -> Observable:
    if len(parts := name.split(".")) == 1:
        shortcut, classname = "", parts[0]
    else:
        shortcut, classname = parts

    if classname not in Observable.all_observables:
        raise ValueError(f"Observable {classname} not found")

    return Observable.all_observables[classname](shortcut, **kwargs)


class Observable(ABC):
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
        if self.shortcut:
            return f"{self.shortcut}.{self.__class__.__name__}"
        else:
            return self.__class__.__name__

    @property
    def value(self) -> Any:
        return self._value

    def to_numpy(self) -> np.ndarray:
        return np.atleast_1d(self.value)

    def __repr__(self) -> str:
        return f"{self.name}: {self.value}"

    def read(self, event: TTree) -> Observable:
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
        ...

    def parse_shortcut(self, shortcut: str) -> list[tuple[str, int | None]]:
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
        for i in alias:
            Observable.all_observables[i] = cls


class Px(Observable):
    def get_value(self) -> Any:
        if len(self.objects) == 0:
            return

        obj = self.objects[0]
        if isinstance(obj, list):
            return [i.P4().Px() for i in obj]
        else:
            return obj.P4().Px()


class Py(Observable):
    def get_value(self) -> Any:
        if len(self.objects) == 0:
            return

        obj = self.objects[0]
        if isinstance(obj, list):
            return [i.P4().Py() for i in obj]
        else:
            return obj.P4().Py()


class Pz(Observable):
    def get_value(self) -> Any:
        if len(self.objects) == 0:
            return

        obj = self.objects[0]
        if isinstance(obj, list):
            return [i.P4().Pz() for i in obj]
        else:
            return obj.P4().Pz()


class E(Observable):
    def get_value(self) -> Any:
        if len(self.objects) == 0:
            return

        obj = self.objects[0]
        if isinstance(obj, list):
            return [i.P4().E() for i in obj]
        else:
            return obj.P4().E()


class Pt(Observable):
    def get_value(self) -> Any:
        if len(self.objects) == 0:
            return

        obj = self.objects[0]
        if isinstance(obj, list):
            return [i.P4().Pt() for i in obj]
        else:
            return obj.P4().Pt()


class Eta(Observable):
    def get_value(self) -> Any:
        if len(self.objects) == 0:
            return

        obj = self.objects[0]
        if isinstance(obj, list):
            return [i.P4().Eta() for i in obj]
        else:
            return obj.P4().Eta()


class Phi(Observable):
    def get_value(self) -> Any:
        if len(self.objects) == 0:
            return

        obj = self.objects[0]
        if isinstance(obj, list):
            return [i.P4().Phi() for i in obj]
        else:
            return obj.P4().Phi()


class M(Observable):
    def get_value(self) -> Any:
        if len(self.objects) == 0:
            return

        obj = self.objects[0]
        if isinstance(obj, list):
            return [i.P4().M() for i in obj]
        else:
            return obj.P4().M()


class DeltaR(Observable):
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
