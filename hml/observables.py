from __future__ import annotations

import re

import numpy as np
from ROOT import TLorentzVector, TTree


def resolve_object_str(object_str: str) -> tuple[list[str], list[int]]:
    """Turn object_str into branches and indices."""
    # Split objects separated by "+", which means combine objects in different branches
    object_strs = object_str.split("+")

    # Resolve each object_str into branch and index
    branches = []
    indices = []
    for object_str in object_strs:
        # object_str is like "Jet0", "Jet1", "Jet2", etc.
        match = re.match(r"([a-z]+)([0-9]*)", object_str, re.I)
        if match:
            items = match.groups()
            # First item is the branch name
            branches.append(items[0])

            if items[1]:
                if int(items[1]) > 0:
                    # Second item is the index + 1, so we need to subtract 1
                    indices.append(int(items[1]) - 1)
                elif int(items[1]) == 0:
                    raise ValueError(f"Numbering of objects starts from 1, not 0")
            else:
                # If no index is given, use -1 to represent all objects in the branch
                indices.append(-1)
        else:
            raise ValueError(f"Invalid object_str: {object_str}")

    return branches, indices


def get_values(
    event: TTree,
    attribute: str,
    branches: list[str],
    indices: list[int],
) -> list[float]:
    """Get the values of attribute of objects in branch."""
    if len(branches) != len(indices):
        raise ValueError("branches and indices must have the same length")

    values = []
    # Get all attribute values in one branch
    if len(indices) == 1 and indices[0] == -1:
        for obj in getattr(event, branches[0]):
            values.append(getattr(obj.P4(), attribute)())
    else:
        # Combine objects in different branches
        combined_object = TLorentzVector()
        for branch, index in zip(branches, indices):
            root_branch = getattr(event, branch)
            if root_branch.GetEntries() <= index:
                raise IndexError(f"Index {index} out of range for branch {branch}")
            combined_object += root_branch[index].P4()
        values.append(getattr(combined_object, attribute)())

    return np.array(values, dtype=np.float32)


class Observable:
    def from_event(self, event: TTree):
        pass


class Px(Observable):
    def __init__(self, object_str: str):
        self._object_str = object_str
        self.name = object_str + "_Px"
        self.values = None

    def from_event(self, event: TTree):
        branches, indices = resolve_object_str(self._object_str)
        self.values = get_values(event, "Px", branches, indices)


class Py(Observable):
    def __init__(self, object_str: str):
        self._object_str = object_str
        self.name = object_str + "_Py"
        self.values = None

    def from_event(self, event: TTree):
        branches, indices = resolve_object_str(self._object_str)
        self.values = get_values(event, "Py", branches, indices)


class Pz(Observable):
    def __init__(self, object_str: str):
        self._object_str = object_str
        self.name = object_str + "_Pz"
        self.values = None

    def from_event(self, event: TTree):
        branches, indices = resolve_object_str(self._object_str)
        self.values = get_values(event, "Pz", branches, indices)


class E(Observable):
    def __init__(self, object_str: str):
        self._object_str = object_str
        self.name = object_str + "_E"
        self.values = None

    def from_event(self, event: TTree):
        branches, indices = resolve_object_str(self._object_str)
        self.values = get_values(event, "E", branches, indices)


class Pt(Observable):
    def __init__(self, object_str: str):
        self._object_str = object_str
        self.name = object_str + "_Pt"
        self.values = None

    def from_event(self, event: TTree):
        branches, indices = resolve_object_str(self._object_str)
        self.values = get_values(event, "Pt", branches, indices)


class Eta(Observable):
    def __init__(self, object_str: str):
        self._object_str = object_str
        self.name = object_str + "_Eta"
        self.values = None

    def from_event(self, event: TTree):
        branches, indices = resolve_object_str(self._object_str)
        self.values = get_values(event, "Eta", branches, indices)


class Phi(Observable):
    def __init__(self, object_str: str):
        self._object_str = object_str
        self.name = object_str + "_Phi"
        self.values = None

    def from_event(self, event: TTree):
        branches, indices = resolve_object_str(self._object_str)
        self.values = get_values(event, "Phi", branches, indices)


class M(Observable):
    def __init__(self, object_str: str):
        self._object_str = object_str
        self.name = object_str + "_M"
        self.values = None

    def from_event(self, event: TTree):
        branches, indices = resolve_object_str(self._object_str)
        self.values = get_values(event, "M", branches, indices)


class DeltaR(Observable):
    def __init__(self, object_str1: str, object_str2: str):
        self._object_str1 = object_str1
        self._object_str2 = object_str2
        self.name = f"DeltaR({object_str1}, {object_str2})"
        self.values = None

    def from_event(self, event: TTree):
        branches1, indices1 = resolve_object_str(self.object_str1)
        eta1 = get_values(event, "Eta", branches1, indices1)
        phi1 = get_values(event, "Phi", branches1, indices1)

        branches2, indices2 = resolve_object_str(self.object_str2)
        eta2 = get_values(event, "Eta", branches2, indices2)
        phi2 = get_values(event, "Phi", branches2, indices2)

        self.values = np.hypot(eta1 - eta2, phi1 - phi2)
