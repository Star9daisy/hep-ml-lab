from __future__ import annotations

import re

import numpy as np
from ROOT import TClonesArray, TLorentzVector, TTree


def resolve_string(s):
    # split the string by '+'
    elements = s.split("+")

    # two lists to store elements and their corresponding numbers
    element_list = []
    number_list = []

    for element in elements:
        # regular expression to find number at the end of each element
        match = re.match(r"([a-z]+)([0-9]*)", element, re.I)
        if match:
            items = match.groups()
            element_list.append(items[0])

            # check if number exists, if not return "no number"
            if items[1] != "":
                number_list.append(int(items[1]))
            else:
                number_list.append("all")

    return element_list, number_list


class Observable:
    pass


class PT:
    def __init__(self, name=""):
        self._name = name
        self._values = None

    def from_event(self, event: TTree):
        names, indices = resolve_string(self._name)

        if indices[0] == "all":
            self._values = [i.PT for i in getattr(event, names[0])]
        else:
            combined_object = TLorentzVector()
            for name, index in zip(names, indices):
                branch = getattr(event, name)
                if branch.GetEntries() <= index + 1:
                    raise IndexError(
                        f"Index {index} out of range for branch {name} with {branch.GetEntries()} entries"
                    )
                combined_object += branch[index].P4()

            self._values = [combined_object.Pt()]

    def from_branch(self, branch: TClonesArray):
        self._values = [i.P4().Pt() for i in branch]

    @property
    def name(self):
        return self._name

    @property
    def values(self):
        return np.array(self._values, dtype=np.float32)

class Mass:
    def __init__(self, name=""):
        self._name = name
        self._values = None

    def from_event(self, event: TTree):
        names, indices = resolve_string(self._name)

        if indices[0] == "all":
            self._values = [i.Mass for i in getattr(event, names[0])]
        else:
            combined_object = TLorentzVector()
            for name, index in zip(names, indices):
                branch = getattr(event, name)
                if branch.GetEntries() <= index + 1:
                    raise IndexError(
                        f"Index {index} out of range for branch {name} with {branch.GetEntries()} entries"
                    )
                combined_object += branch[index].P4()

            self._values = [combined_object.M()]

    def from_branch(self, branch: TClonesArray):
        self._values = [i.P4().M() for i in branch]

    @property
    def name(self):
        return self._name

    @property
    def values(self):
        return np.array(self._values, dtype=np.float32)


class Eta:
    def __init__(self, name=""):
        self._name = name
        self._values = None

    def from_event(self, event: TTree):
        names, indices = resolve_string(self._name)

        if indices[0] == "all":
            self._values = [i.Eta for i in getattr(event, names[0])]
        else:
            combined_object = TLorentzVector()
            for name, index in zip(names, indices):
                branch = getattr(event, name)
                if branch.GetEntries() <= index + 1:
                    raise IndexError(
                        f"Index {index} out of range for branch {name} with {branch.GetEntries()} entries"
                    )
                combined_object += branch[index].P4()

            self._values = [combined_object.Eta()]

    def from_branch(self, branch: TClonesArray):
        self._values = [i.P4().Eta() for i in branch]

    @property
    def name(self):
        return self._name

    @property
    def values(self):
        return np.array(self._values, dtype=np.float32)