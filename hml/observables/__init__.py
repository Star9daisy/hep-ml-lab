from .azimuthal_angle import AzimuthalAngle
from .azimuthal_angle import Phi
from .b_tag import BTag
from .charge import Charge
from .energy import E
from .energy import Energy
from .invariant_mass import InvariantMass
from .invariant_mass import InvM
from .invariant_mass import InvMass
from .mass import M
from .mass import Mass
from .momentum_x import MomentumX
from .momentum_x import Px
from .momentum_y import MomentumY
from .momentum_y import Py
from .momentum_z import MomentumZ
from .momentum_z import Pz
from .n_subjettiness import NSubjettiness
from .n_subjettiness import TauN
from .n_subjettiness_ratio import NSubjettinessRatio
from .n_subjettiness_ratio import TauMN
from .observable import Observable
from .pseudo_rapidity import Eta
from .pseudo_rapidity import PseudoRapidity
from .size import Size
from .tau_tag import TauTag
from .transverse_momentum import Pt
from .transverse_momentum import TransverseMomentum


def get(identifier: str | None, *arg, **kwarg):
    if identifier == "" or identifier is None:
        return None

    if "." in identifier:
        # Each nested physics object has one dot, so there may be multiple dots.
        # So we only take the last dot as the separator between physics object
        # and observable name.
        physics_object = ".".join(identifier.split(".")[:-1])
        name = identifier.split(".")[-1]
        kwarg["physics_object"] = physics_object

        # Check if the observable name is a valid NSubjettiness
        if name.startswith("Tau") or name.startswith("tau") or name.startswith("tau_"):
            if name[-2].isdigit():
                m = int(name[-2])
                n = int(name[-1])
                return TauMN(m, n, physics_object, name)
            if name[-1].isdigit():
                n = int(name[-1])
                return TauN(n, physics_object, name)

        identifier = name

    if identifier not in Observable.ALL_OBSERVABLES:
        return None
    else:
        return Observable.ALL_OBSERVABLES[identifier](*arg, **kwarg)
