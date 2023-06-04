from __future__ import annotations

import re
from itertools import product

import numpy as np
from ROOT import TClonesArray, TLorentzVector, TTree


def resolve_string(s, sep="+"):
    # split the string by '+'
    elements = s.split(sep)

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


class Px(Observable):
    def __init__(self, name=""):
        self._name = name
        self._values = None

    def from_event(self, event: TTree):
        names, indices = resolve_string(self._name)

        if indices[0] == "all":
            self._values = [i.P4().Px() for i in getattr(event, names[0])]
        else:
            combined_object = TLorentzVector()
            for name, index in zip(names, indices):
                branch = getattr(event, name)
                if branch.GetEntries() <= index + 1:
                    raise IndexError(
                        f"Index {index} out of range for branch {name} with {branch.GetEntries()} entries"
                    )
                combined_object += branch[index].P4()

            self._values = [combined_object.Px()]

    def from_branch(self, branch: TClonesArray):
        self._values = [i.P4().Px() for i in branch]

    @property
    def name(self):
        return self._name

    @property
    def values(self):
        return np.array(self._values, dtype=np.float32)


class Py(Observable):
    def __init__(self, name=""):
        self._name = name
        self._values = None

    def from_event(self, event: TTree):
        names, indices = resolve_string(self._name)

        if indices[0] == "all":
            self._values = [i.P4().Py() for i in getattr(event, names[0])]
        else:
            combined_object = TLorentzVector()
            for name, index in zip(names, indices):
                branch = getattr(event, name)
                if branch.GetEntries() <= index + 1:
                    raise IndexError(
                        f"Index {index} out of range for branch {name} with {branch.GetEntries()} entries"
                    )
                combined_object += branch[index].P4()

            self._values = [combined_object.Py()]

    def from_branch(self, branch: TClonesArray):
        self._values = [i.P4().Py() for i in branch]

    @property
    def name(self):
        return self._name

    @property
    def values(self):
        return np.array(self._values, dtype=np.float32)


class Pz(Observable):
    def __init__(self, name=""):
        self._name = name
        self._values = None

    def from_event(self, event: TTree):
        names, indices = resolve_string(self._name)

        if indices[0] == "all":
            self._values = [i.P4().Pz() for i in getattr(event, names[0])]
        else:
            combined_object = TLorentzVector()
            for name, index in zip(names, indices):
                branch = getattr(event, name)
                if branch.GetEntries() <= index + 1:
                    raise IndexError(
                        f"Index {index} out of range for branch {name} with {branch.GetEntries()} entries"
                    )
                combined_object += branch[index].P4()

            self._values = [combined_object.Pz()]

    def from_branch(self, branch: TClonesArray):
        self._values = [i.P4().Pz() for i in branch]

    @property
    def name(self):
        return self._name

    @property
    def values(self):
        return np.array(self._values, dtype=np.float32)


class E(Observable):
    def __init__(self, name=""):
        self._name = name
        self._values = None

    def from_event(self, event: TTree):
        names, indices = resolve_string(self._name)

        if indices[0] == "all":
            self._values = [i.P4().E() for i in getattr(event, names[0])]
        else:
            combined_object = TLorentzVector()
            for name, index in zip(names, indices):
                branch = getattr(event, name)
                if branch.GetEntries() <= index + 1:
                    raise IndexError(
                        f"Index {index} out of range for branch {name} with {branch.GetEntries()} entries"
                    )
                combined_object += branch[index].P4()

            self._values = [combined_object.E()]

    def from_branch(self, branch: TClonesArray):
        self._values = [i.P4().E() for i in branch]

    @property
    def name(self):
        return self._name

    @property
    def values(self):
        return np.array(self._values, dtype=np.float32)


class PT(Observable):
    def __init__(self, name=""):
        self._name = name
        self._values = None

    def from_event(self, event: TTree):
        names, indices = resolve_string(self._name)

        if indices[0] == "all":
            self._values = [i.P4().Pt() for i in getattr(event, names[0])]
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


class Eta(Observable):
    def __init__(self, name=""):
        self._name = name
        self._values = None

    def from_event(self, event: TTree):
        names, indices = resolve_string(self._name)

        if indices[0] == "all":
            self._values = [i.P4().Eta() for i in getattr(event, names[0])]
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


class Phi(Observable):
    def __init__(self, name=""):
        self._name = name
        self._values = None

    def from_event(self, event: TTree):
        names, indices = resolve_string(self._name)

        if indices[0] == "all":
            self._values = [i.P4().Phi() for i in getattr(event, names[0])]
        else:
            combined_object = TLorentzVector()
            for name, index in zip(names, indices):
                branch = getattr(event, name)
                if branch.GetEntries() <= index + 1:
                    raise IndexError(
                        f"Index {index} out of range for branch {name} with {branch.GetEntries()} entries"
                    )
                combined_object += branch[index].P4()

            self._values = [combined_object.Phi()]

    def from_branch(self, branch: TClonesArray):
        self._values = [i.P4().Phi() for i in branch]

    @property
    def name(self):
        return self._name

    @property
    def values(self):
        return np.array(self._values, dtype=np.float32)


class M(Observable):
    def __init__(self, name=""):
        self._name = name
        self._values = None

    def from_event(self, event: TTree):
        names, indices = resolve_string(self._name)

        if indices[0] == "all":
            self._values = [i.P4().M() for i in getattr(event, names[0])]
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


class DeltaR(Observable):
    def __init__(self, name=""):
        self._name = name
        self._values = None

    def from_event(self, event: TTree):
        names, indices = resolve_string(self._name, sep="-")

        objects = []
        for name, index in zip(names, indices):
            if index == "all":
                objects.append([i.P4() for i in getattr(event, name)])
            else:
                objects.append([getattr(event, name)[index].P4()])

        values = np.array([i.DeltaR(j) for i, j in product(*objects)], dtype=np.float32)
        length1, length2 = len(objects[0]), len(objects[1])
        self._values = values.reshape(length1, length2)

    def from_branches(self, branches: list[TClonesArray]):
        if len(branches) != 2:
            raise ValueError("DeltaR observable requires exactly two branches")

        array1 = [i.P4() for i in branches[0]]
        array2 = [i.P4() for i in branches[1]]
        values = np.array([i.DeltaR(j) for i, j in product(array1, array2)], dtype=np.float32)
        length1, length2 = len(array1), len(array2)
        self._values = values.reshape(length1, length2)

    @property
    def name(self):
        return self._name

    @property
    def values(self):
        return self._values


TransverseMomentum = PT
PseudoRapidity = Eta
AzimuthalAngle = Phi
Mass = M
