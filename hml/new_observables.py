from __future__ import annotations

import numpy as np
from ROOT import TTree  # type: ignore


class Observable:
    all_observables = {}

    def __init__(
        self,
        name: str | None = None,
        value: float | list[float] | None = None,
        **kwargs,
    ):
        self._name = name
        self._value = value
        self.other_params = kwargs

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        Observable.all_observables.update({cls.__name__: cls})

    @classmethod
    def register(cls, name: str) -> None:
        Observable.all_observables.update({name: cls})

    @property
    def name(self) -> str | None:
        return self._name

    @property
    def value(self) -> float | list[float] | None:
        return self._value

    def to_numpy(self) -> np.ndarray:
        return np.atleast_1d(np.array(self.value))

    def update(self, event: TTree) -> Observable:
        if (parts := self.resolve_name()) is None:
            return self

        branch_name, leaf_name, index = parts
        self.branch = getattr(event, branch_name)
        self.leaf_names = [i.GetName() for i in event.GetListOfLeaves()]

        # Check if the observable is already defined in this file
        if leaf_name in Observable.all_observables:
            obs = Observable.all_observables[leaf_name](**self.other_params)
            obs.update(event)
            self._value = obs.value
            return self

        # Check if the leaf_name exists in the leaf names
        if f"{branch_name}.{leaf_name}" in self.leaf_names:
            if index is None:
                self._value = [getattr(i, leaf_name) for i in self.branch]
            else:
                self._value = getattr(self.branch[index], leaf_name)
        else:
            if index is None:
                lorentz = [i.P4() for i in self.branch]
                self._value = [getattr(i, leaf_name)() for i in lorentz]
            else:
                lorentz = self.branch[index].P4()
                self._value = getattr(lorentz, leaf_name)()
        return self

    def __repr__(self):
        return f"{self.name}: {self.value}"

    def resolve_name(self):
        if self.name is None:
            return

        prefices, leaf_name = self.name.split(".")

        if len(parts := prefices.split("_")) == 1:
            branch_name = parts[0]
            index = None
        elif len(parts) == 2:
            branch_name, index = parts
            index = int(index)
        else:
            raise ValueError("Invalid observable name")

        return branch_name, leaf_name, index


class Tau21(Observable):
    def __init__(self):
        super().__init__("Tau21")

    def update(self, event: TTree) -> Observable:
        self._value = event.FatJet[0].Tau[1] / event.FatJet[0].Tau[0]
        return self


class NSubjettinessRatio(Observable):
    def __init__(self, m, n):
        super().__init__(f"Tau{m}{n}")
        self.m = m
        self.n = n

    def update(self, event: TTree) -> Observable:
        self._value = event.FatJet[0].Tau[self.m - 1] / event.FatJet[0].Tau[self.n - 1]
        return self


# alias
NSubjettinessRatio.register("TauMN")
