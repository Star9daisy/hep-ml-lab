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
        self._separator_between_branch_name_and_index = "_"
        self._separator_between_objects = "-"

        if shortcut:
            self.shortcut = shortcut
            self.object_pairs = self.parse_shortcut(shortcut)
        elif object_pairs:
            self.shortcut = self.build_shortcut(object_pairs)
            self.object_pairs = object_pairs
        else:
            raise ValueError("Must provide either shortcut or object_pairs")

        self._name = f"{self.shortcut}.{self.__class__.__name__}"
        self._value = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def value(self) -> Any:
        return self._value

    def to_array(self) -> np.ndarray:
        return np.atleast_1d(self.value)

    def __repr__(self) -> str:
        return f"{self.name}: {self.value}"

    def read(self, event: TTree) -> Observable:
        self.objects = []
        for branch_name, index in self.object_pairs:
            if branch_name not in event.GetListOfBranches():
                raise ValueError(f"Branch {branch_name} not found in event")

            branch = getattr(event, branch_name)
            if index is None:
                self.objects.append([i for i in branch])
            else:
                if index >= branch.GetEntries():
                    raise ValueError(
                        f"Index {index} out of range for branch {branch_name}"
                    )
                else:
                    self.objects.append(branch[index])

        return self

    @abstractmethod
    def update(self) -> Observable:
        return self

    def parse_shortcut(self, shortcut: str) -> list[tuple[str, int | None]]:
        object_pairs = []
        objects = shortcut.split(self._separator_between_objects)
        for obj in objects:
            if "_" in obj:
                branch_name, index = obj.split(
                    self._separator_between_branch_name_and_index
                )
                index = int(index)
            else:
                branch_name, index = obj, None

            object_pairs.append((branch_name, index))
        return object_pairs

    def build_shortcut(self, object_pairs: list[tuple[str, int | None]]) -> str:
        shortcuts = []
        for branch_name, index in object_pairs:
            if index is not None:
                obj = f"{branch_name}{self._separator_between_branch_name_and_index}{index}"
            else:
                obj = branch_name
            shortcuts.append(obj)
        return self._separator_between_objects.join(shortcuts)

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        Observable.all_observables[cls.__name__] = cls

    @classmethod
    def add_alias(cls, *alias: str) -> None:
        for i in alias:
            Observable.all_observables[i] = cls


class Px(Observable):
    def update(self) -> Px:
        obj = self.objects[0]
        if isinstance(obj, list):
            self._value = [i.P4().Px() for i in obj]
        else:
            self._value = obj.P4().Px()

        return self


class Py(Observable):
    def update(self) -> Py:
        obj = self.objects[0]
        if isinstance(obj, list):
            self._value = [i.P4().Py() for i in obj]
        else:
            self._value = obj.P4().Py()

        return self


class Pz(Observable):
    def update(self) -> Pz:
        obj = self.objects[0]
        if isinstance(obj, list):
            self._value = [i.P4().Pz() for i in obj]
        else:
            self._value = obj.P4().Pz()

        return self


class E(Observable):
    def update(self) -> E:
        obj = self.objects[0]
        if isinstance(obj, list):
            self._value = [i.P4().E() for i in obj]
        else:
            self._value = obj.P4().E()

        return self


class Eta(Observable):
    def update(self) -> Eta:
        obj = self.objects[0]
        if isinstance(obj, list):
            self._value = [i.P4().Eta() for i in obj]
        else:
            self._value = obj.P4().Eta()

        return self


class Phi(Observable):
    def update(self) -> Phi:
        obj = self.objects[0]
        if isinstance(obj, list):
            self._value = [i.P4().Phi() for i in obj]
        else:
            self._value = obj.P4().Phi()

        return self


class Pt(Observable):
    def update(self) -> Pt:
        obj = self.objects[0]
        if isinstance(obj, list):
            self._value = [i.P4().Pt() for i in obj]
        else:
            self._value = obj.P4().Pt()

        return self


class M(Observable):
    def update(self) -> M:
        obj = self.objects[0]
        if isinstance(obj, list):
            self._value = [i.P4().M() for i in obj]
        else:
            self._value = obj.P4().M()

        return self


class DeltaR(Observable):
    def update(self) -> Observable:
        obj1, obj2 = self.objects[:2]
        obj1 = [obj1] if not isinstance(obj1, list) else obj1
        obj2 = [obj2] if not isinstance(obj2, list) else obj2

        distances = []
        for i, j in product(obj1, obj2):
            distances.append(i.P4().DeltaR(j.P4()))

        self._value = distances[0] if len(distances) == 1 else distances

        return self


class NSubjettiness(Observable):
    def __init__(
        self,
        shortcut: str | None = None,
        object_pairs: list[tuple[str, int | None]] | None = None,
        n: int = 1,
    ) -> None:
        super().__init__(shortcut, object_pairs)
        self.n = n

    def update(self) -> Observable:
        obj = self.objects[0]
        if isinstance(obj, list):
            self._value = [i.Tau[self.n - 1] for i in obj]
        else:
            self._value = obj.Tau[self.n - 1]

        return self


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

    def update(self) -> Observable:
        obj = self.objects[0]
        if isinstance(obj, list):
            self._value = [i.Tau[self.m - 1] / i.Tau[self.n - 1] for i in obj]
        else:
            self._value = obj.Tau[self.m - 1] / obj.Tau[self.n - 1]

        return self


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
