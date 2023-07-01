from __future__ import annotations

import re
from typing import Protocol

import numpy as np
from ROOT import TLorentzVector, TTree
from typing_extensions import runtime_checkable


def resolve_shortname(shortname: str) -> tuple[list[str], list[int]]:
    """Turn shortname into branches and indices.

    A shortname represents a indexed object in a branch, e.g. "Jet1", "Muon1", "Jet1+Muon1".
    """
    # Split shortname by "+" to get all single objects
    shortnames = shortname.split("+")

    # Resolve each shortname into branch and index
    branches = []
    indices = []
    for shortname in shortnames:
        match = re.match(r"([a-z]+)([0-9]*)", shortname, re.I)
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
            raise ValueError(f"Invalid shortname: {shortname}")

    return branches, indices


def get_lorentzvector_values(
    event: TTree,
    attribute: str,
    branches: list[str],
    indices: list[int],
) -> np.ndarray:
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


@runtime_checkable
class Observable(Protocol):
    def from_event(self, event: TTree):
        pass # pragma: no cover


class Px(Observable):
    def __init__(self, shortname: str):
        self._shortname = shortname
        self.name = shortname + "_Px"
        self.values = None

    def from_event(self, event: TTree):
        branches, indices = resolve_shortname(self._shortname)
        self.values = get_lorentzvector_values(event, "Px", branches, indices)


class Py(Observable):
    def __init__(self, shortname: str):
        self._shortname = shortname
        self.name = shortname + "_Py"
        self.values = None

    def from_event(self, event: TTree):
        branches, indices = resolve_shortname(self._shortname)
        self.values = get_lorentzvector_values(event, "Py", branches, indices)


class Pz(Observable):
    def __init__(self, shortname: str):
        self._shortname = shortname
        self.name = shortname + "_Pz"
        self.values = None

    def from_event(self, event: TTree):
        branches, indices = resolve_shortname(self._shortname)
        self.values = get_lorentzvector_values(event, "Pz", branches, indices)


class E(Observable):
    def __init__(self, shortname: str):
        self._shortname = shortname
        self.name = shortname + "_E"
        self.values = None

    def from_event(self, event: TTree):
        branches, indices = resolve_shortname(self._shortname)
        self.values = get_lorentzvector_values(event, "E", branches, indices)


class Pt(Observable):
    def __init__(self, shortname: str):
        self._shortname = shortname
        self.name = shortname + "_Pt"
        self.values = None

    def from_event(self, event: TTree):
        branches, indices = resolve_shortname(self._shortname)
        self.values = get_lorentzvector_values(event, "Pt", branches, indices)


class Eta(Observable):
    def __init__(self, shortname: str):
        self._shortname = shortname
        self.name = shortname + "_Eta"
        self.values = None

    def from_event(self, event: TTree):
        branches, indices = resolve_shortname(self._shortname)
        self.values = get_lorentzvector_values(event, "Eta", branches, indices)


class Phi(Observable):
    def __init__(self, shortname: str):
        self._shortname = shortname
        self.name = shortname + "_Phi"
        self.values = None

    def from_event(self, event: TTree):
        branches, indices = resolve_shortname(self._shortname)
        self.values = get_lorentzvector_values(event, "Phi", branches, indices)


class M(Observable):
    def __init__(self, shortname: str):
        self._shortname = shortname
        self.name = shortname + "_M"
        self.values = None

    def from_event(self, event: TTree):
        branches, indices = resolve_shortname(self._shortname)
        self.values = get_lorentzvector_values(event, "M", branches, indices)


class DeltaR(Observable):
    def __init__(self, shortname1: str, shortname2: str):
        self._shortname1 = shortname1
        self._shortname2 = shortname2
        self.name = f"DeltaR({shortname1}, {shortname2})"
        self.values = None

    def from_event(self, event: TTree):
        branches1, indices1 = resolve_shortname(self._shortname1)
        eta1 = get_lorentzvector_values(event, "Eta", branches1, indices1)
        phi1 = get_lorentzvector_values(event, "Phi", branches1, indices1)

        branches2, indices2 = resolve_shortname(self._shortname2)
        eta2 = get_lorentzvector_values(event, "Eta", branches2, indices2)
        phi2 = get_lorentzvector_values(event, "Phi", branches2, indices2)

        self.values = np.hypot(eta1 - eta2, phi1 - phi2)
