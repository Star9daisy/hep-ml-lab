from __future__ import annotations

from abc import ABC, abstractmethod
from functools import reduce
from itertools import product
from typing import Any

import numpy as np
from ROOT import TTree  # type: ignore


def get_observable(name: str, **kwargs) -> Observable:
    """Get an observable according to its name.

    An observable name is composed of two parts: the physics object and the
    observable class.

    For example:

    1. `Jet_0.Pt`: `Jet_0` is the single physics object (the
    leading jet), and `Pt` is the observable class (TransverseMomentum);
    2. `Electron.Charge`: `Electron` is the collective physics objects (all
    electrons), and `Charge` is the observable class;
    3. `Particle-FatJet_0.DeltaR`: `Particle-FatJet_0` are the multiple physics
    objects (all particles and the leading FatJet), and `DeltaR` is the
    observable class (AngularDistance). It calculates the angular distance
    between each particle and the leading FatJet.
    """
    if len(parts := name.split(".")) == 1:
        phyobj, classname = "", parts[0]
    else:
        phyobj, classname = parts

    if classname not in Observable.all_observables:
        raise ValueError(f"Observable {classname} not found")

    return Observable.all_observables[classname](phyobj, name=classname, **kwargs)


class Observable(ABC):
    """Base class for observables.

    Implement the `get_value` method to define a new observable.
    """

    all_observables = {}

    def __init__(
        self,
        phyobj: str | None = None,
        phyobj_pairs: list[tuple[str, int | None]] | None = None,
        name: str | None = None,
    ) -> None:
        self.sep_for_branch_and_index = "_"
        self.sep_for_phyobjs = "-"

        if phyobj:
            self.phyobj = phyobj
            self.phyobj_pairs = self.parse_phyobj(phyobj)
        elif phyobj_pairs:
            self.phyobj = self.build_phyobj(phyobj_pairs)
            self.phyobj_pairs = phyobj_pairs
        else:
            self.phyobj = None
            self.phyobj_pairs = None

        self._name = self.__class__.__name__ if name is None else name
        self._value = None

    @property
    def name(self) -> str:
        """The name of the observable.

        The name is composed of the physics object and the class name, e.g.
        `Jet_0.Pt`.
        """
        if self.phyobj:
            return f"{self.phyobj}.{self._name}"
        else:
            return self._name

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

    def read(self, event: TTree) -> Observable:
        """Read an event and fetch the physics objects.

        It creates three attributes: event, objects and _value. The _value is
        calculated by calling the `get_value` method.
        """
        self.event = event
        self.phyobjs = []
        self._value = None

        if self.phyobj_pairs:
            for branch_name, index in self.phyobj_pairs:
                if branch_name in event.GetListOfBranches():
                    branch = getattr(event, branch_name)

                    if index is None:
                        self.phyobjs.append([i for i in branch])
                    elif index < branch.GetEntries():
                        self.phyobjs.append(branch[index])

        self._value = self.get_value()

        return self

    @abstractmethod
    def get_value(self) -> Any:
        """Calculate the value of the observable.

        Implement this method to define a new observable. Here're common cases:
        1. Quick calculation: use `self.event` to get physics objects and write
        the calculation directly.
        2. Take the advantage of Observable: use `self.phyobjs` to do the
        calculation.

        Return None if the observable is not correctly got.
        """
        ...  # pragma: no cover

    def parse_phyobj(self, phyobj: str) -> list[tuple[str, int | None]]:
        """Parse the physics object string to get their pairs."""
        phyobj_pairs = []
        phyobjs = phyobj.split(self.sep_for_phyobjs)
        for obj in phyobjs:
            if "_" in obj:
                branch_name, index = obj.split(self.sep_for_branch_and_index)
                index = int(index)
            else:
                branch_name, index = obj, None

            phyobj_pairs.append((branch_name, index))
        return phyobj_pairs

    def build_phyobj(self, phyobj_pairs: list[tuple[str, int | None]]) -> str:
        """Build the observable name from the physics object pairs."""
        phyobjs = []
        for branch_name, index in phyobj_pairs:
            if index is not None:
                obj = f"{branch_name}{self.sep_for_branch_and_index}{index}"
            else:
                obj = branch_name
            phyobjs.append(obj)
        return self.sep_for_phyobjs.join(phyobjs)

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        Observable.all_observables[cls.__name__] = cls

    @classmethod
    def add_alias(cls, *alias: str) -> None:
        """Add alias for the class name."""
        for i in alias:
            Observable.all_observables[i] = cls


# MomentumX ------------------------------------------------------------------ #
class MomentumX(Observable):
    """Get the x component of the momentum.

    Available for single and collective physics objects. For example:
    - `Jet_0.Px` is the x component of the momentum of the leading jet.
    - `Jet.Px` is the x component of the momentum of all jets.

    Alias: momentum_x, Px, px
    """

    def get_value(self) -> float | list[float] | None:
        if len(self.phyobjs) == 0:
            return

        obj = self.phyobjs[0]
        if isinstance(obj, list):
            return [i.P4().Px() for i in obj]
        else:
            return obj.P4().Px()


class Px(MomentumX):
    pass


# MomentumY ------------------------------------------------------------------ #
class MomentumY(Observable):
    """Get the y component of the momentum.

    Available for single and collective physics objects. For example:
    - `Jet_0.Py` is the y component of the momentum of the leading jet.
    - `Jet.Py` is the y component of the momentum of all jets.

    Alias: momentum_y, Py, py
    """

    def get_value(self) -> float | list[float] | None:
        if len(self.phyobjs) == 0:
            return

        obj = self.phyobjs[0]
        if isinstance(obj, list):
            return [i.P4().Py() for i in obj]
        else:
            return obj.P4().Py()


class Py(MomentumY):
    pass


# MomentumZ ------------------------------------------------------------------ #
class MomentumZ(Observable):
    """Get the z component of the momentum.

    Available for single and collective physics objects. For example:
    - `Jet_0.Pz` is the z component of the momentum of the leading jet.
    - `Jet.Pz` is the z component of the momentum of all jets.

    Alias: momentum_z, Pz, pz
    """

    def get_value(self) -> float | list[float] | None:
        if len(self.phyobjs) == 0:
            return

        obj = self.phyobjs[0]
        if isinstance(obj, list):
            return [i.P4().Pz() for i in obj]
        else:
            return obj.P4().Pz()


class Pz(MomentumZ):
    pass


# Energy --------------------------------------------------------------------- #
class Energy(Observable):
    """Get the energy of the object.

    Available for single and collective physics objects. For example:
    - `Jet_0.E` is the energy of the leading jet.
    - `Jet.E` is the energy of all jets.

    Alias: energy, E, e
    """

    def get_value(self) -> float | list[float] | None:
        if len(self.phyobjs) == 0:
            return

        obj = self.phyobjs[0]
        if isinstance(obj, list):
            return [i.P4().E() for i in obj]
        else:
            return obj.P4().E()


class E(Energy):
    pass


# TransverseMomentum --------------------------------------------------------- #
class TransverseMomentum(Observable):
    """Get the transverse momentum of the object.

    Available for single and collective physics objects. For example:
    - `Jet_0.Pt` is the transverse momentum of the leading jet.
    - `Jet.Pt` is the transverse momentum of all jets.

    Alias: transverse_momentum, PT, Pt, pT, pt
    """

    def get_value(self) -> float | list[float] | None:
        if len(self.phyobjs) == 0:
            return

        obj = self.phyobjs[0]
        if isinstance(obj, list):
            return [i.P4().Pt() for i in obj]
        else:
            return obj.P4().Pt()


class Pt(TransverseMomentum):
    pass


# PseudoRapidity ------------------------------------------------------------- #
class PseudoRapidity(Observable):
    """Get the pseudo-rapidity of the object.

    Available for single and collective physics objects. For example:
    - `Jet_0.Eta` is the pseudorapidity of the leading jet.
    - `Jet.Eta` is the pseudorapidity of all jets.

    Alias: eta
    """

    def get_value(self) -> float | list[float] | None:
        if len(self.phyobjs) == 0:
            return

        obj = self.phyobjs[0]
        if isinstance(obj, list):
            return [i.P4().Eta() for i in obj]
        else:
            return obj.P4().Eta()


class Eta(PseudoRapidity):
    pass


# AzimuthalAngle ------------------------------------------------------------- #
class AzimuthalAngle(Observable):
    """Get the azimuthal angle of the object.

    Available for single and collective physics objects. For example:
    - `Jet_0.Phi` is the azimuthal angle of the leading jet.
    - `Jet.Phi` is the azimuthal angle of all jets.

    Alias: azimuthal_angle, Phi, phi
    """

    def get_value(self) -> float | list[float] | None:
        if len(self.phyobjs) == 0:
            return

        obj = self.phyobjs[0]
        if isinstance(obj, list):
            return [i.P4().Phi() for i in obj]
        else:
            return obj.P4().Phi()


class Phi(AzimuthalAngle):
    pass


# Mass ----------------------------------------------------------------------- #
class Mass(Observable):
    """Get the mass of the object.

    Available for single and collective physics objects. For example:
    - `Jet_0.M` is the mass of the leading jet.
    - `Jet.M` is the mass of all jets.

    Alias: mass, M, m
    """

    def get_value(self) -> float | list[float] | None:
        if len(self.phyobjs) == 0:
            return

        obj = self.phyobjs[0]
        if isinstance(obj, list):
            return [i.P4().M() for i in obj]
        else:
            return obj.P4().M()


class M(Mass):
    pass


# NSubjettiness -------------------------------------------------------------- #
class NSubjettiness(Observable):
    """Get the n-subjettiness from the leaf Tau of the branch FatJet.

    Available for single and collective FatJet objects. For example:
    - `FatJet_0.NSubjettiness` is the tau1 (by default) of the leading FatJet.
    - `FatJet.NSubjettiness` is the tau1 of all FatJets.

    Alias: n_subjettiness, TauN, tau_n
    """

    def __init__(
        self,
        phyobj: str | None = None,
        phyobj_pairs: list[tuple[str, int | None]] | None = None,
        n: int = 1,
        **kwargs,
    ) -> None:
        super().__init__(phyobj, phyobj_pairs, **kwargs)
        self.n = n

    def get_value(self) -> float | list[float] | None:
        if len(self.phyobjs) == 0:
            return

        obj = self.phyobjs[0]
        if isinstance(obj, list):
            return [i.Tau[self.n - 1] for i in obj]
        else:
            return obj.Tau[self.n - 1]


class TauN(NSubjettiness):
    pass


# NSubjettinessRatio --------------------------------------------------------- #
class NSubjettinessRatio(Observable):
    """Calculate the n-subjettiness ratio from the leaf Tau of the branch FatJet.

    Available for single and collective FatJet objects. For example:
    - `FatJet_0.NSubjettinessRatio` is the tau21 (by default) of the leading
    - `FatJet.NSubjettinessRatio` is the tau21 of all FatJets.
    FatJet.

    Alias: n_subjetiness_ratio, TauMN, tau_mn
    """

    def __init__(
        self,
        phyobj: str | None = None,
        phyobj_pairs: list[tuple[str, int | None]] | None = None,
        m: int = 2,
        n: int = 1,
        **kwargs,
    ) -> None:
        super().__init__(phyobj, phyobj_pairs, **kwargs)
        self.m = m
        self.n = n

    def get_value(self) -> float | list[float] | None:
        if len(self.phyobjs) == 0:
            return

        obj = self.phyobjs[0]
        if isinstance(obj, list):
            value = []
            for i in obj:
                if i.Tau[self.n - 1] == 0:
                    value.append(float("nan"))
                else:
                    value.append(i.Tau[self.m - 1] / i.Tau[self.n - 1])
        else:
            if obj.Tau[self.n - 1] == 0:
                value = float("nan")
            else:
                value = obj.Tau[self.m - 1] / obj.Tau[self.n - 1]

        return value


class TauMN(NSubjettinessRatio):
    pass


# BTag ----------------------------------------------------------------------- #
class BTag(Observable):
    """Get the b-tag of the physics object.

    Available for single and collective physics objects. For example:
    - `Jet_0.BTag` is the b-tag of the leading jet.
    - `Jet.BTag` is the b-tag of all jets.

    Alias: b_tag
    """

    def get_value(self) -> float | list[float] | None:
        if len(self.phyobjs) == 0:
            return

        obj = self.phyobjs[0]

        if isinstance(obj, list):
            return [i.BTag for i in obj]
        else:
            return obj.BTag


# Charge --------------------------------------------------------------------- #
class Charge(Observable):
    """Get the charge of the object.

    Available for single and collective physics objects. For example:
    - `Electron_0.Charge` is the charge of the leading electron.
    - `Electron.Charge` is the charge of all electrons.

    Alias: charge
    """

    def get_value(self) -> float | list[float] | None:
        if len(self.phyobjs) == 0:
            return

        obj = self.phyobjs[0]

        if isinstance(obj, list):
            return [i.Charge for i in obj]
        else:
            return obj.Charge


# Size ----------------------------------------------------------------------- #
class Size(Observable):
    """The number of physics objects.

    Available for collective object. For example:
    - `Jet.Size` is the number of jets.

    Alias: size
    """

    def get_value(self) -> float | list[float] | None:
        if len(self.phyobjs) > 0:
            return len(self.phyobjs[0])


# InvariantMass -------------------------------------------------------------- #
class InvariantMass(Observable):
    """Get the invariant mass of the object.

    Available for single and multiple physics objects. When it is the single
    case, InvariantMass is the same as Mass. For example:
    - `Jet_0.InvariantMass` is the same as `Jet_0.Mass`.
    - `Electron_0-Jet_0.InvariantMass` is the invariant mass of the leading
        electron and leading jet.

    Alias: invariant_mass, InvMass, inv_mass, InvM, inv_m
    """

    def get_value(self) -> float | list[float] | None:
        for obj in self.phyobjs:
            if isinstance(obj, list):
                raise ValueError(
                    "InvariantMass is not available for collective objects"
                )

        return reduce(lambda i, j: i.P4() + j.P4(), self.phyobjs).M()


class InvMass(InvariantMass):
    pass


class InvM(InvariantMass):
    pass


# AngularDistance ------------------------------------------------------------ #
class AngularDistance(Observable):
    """Calculate the angular distance between two objects.

    Available for multiple(two) physics objects. For example:
    - `Jet_0-Jet_1.DeltaR` is the deltaR between the leading two jets.
    - `Jet_0-Jet.DeltaR` is the deltaR between the leading jet and all jets.
    - `Jet-Jet.DeltaR` is the deltaR between all jets.

    Alias: angular_distance, DeltaR, delta_r
    """

    def get_value(self) -> float | list[float] | list[list[float]] | None:
        if len(self.phyobjs) != 2:
            return

        obj1, obj2 = self.phyobjs
        obj1 = [obj1] if not isinstance(obj1, list) else obj1
        obj2 = [obj2] if not isinstance(obj2, list) else obj2

        distances = []
        for i, j in product(obj1, obj2):
            distances.append(i.P4().DeltaR(j.P4()))

        return distances[0] if len(distances) == 1 else distances


class DeltaR(AngularDistance):
    pass


# Alias ---------------------------------------------------------------------- #
# Px, Py, Pz, E
MomentumX.add_alias("momentum_x")
MomentumY.add_alias("momentum_y")
MomentumZ.add_alias("momentum_z")
Energy.add_alias("energy")
Px.add_alias("px")
Py.add_alias("py")
Pz.add_alias("pz")
E.add_alias("e")

# Pt, Eta, Phi, M
TransverseMomentum.add_alias("transverse_momentum")
PseudoRapidity.add_alias("pseudo_rapidity")
AzimuthalAngle.add_alias("azimuthal_angle")
Mass.add_alias("mass")
Pt.add_alias("PT", "pT", "pt")
Eta.add_alias("eta")
Phi.add_alias("phi")
M.add_alias("m")

# Other leaves
BTag.add_alias("b_tag")
Charge.add_alias("charge")
Size.add_alias("size")

# NSubjettiness
NSubjettiness.add_alias("n_subjettiness")
NSubjettinessRatio.add_alias("n_subjetiness_ratio")
TauN.add_alias("tau_n")
TauMN.add_alias("tau_mn")

# Custom
InvariantMass.add_alias("invariant_mass")
InvMass.add_alias("inv_mass")
InvM.add_alias("inv_m")

AngularDistance.add_alias("angular_distance")
DeltaR.add_alias("delta_r")
