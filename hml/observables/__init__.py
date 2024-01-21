from .n_subjettiness import NSubjettiness
from .n_subjettiness import TauN
from .n_subjettiness_ratio import NSubjettinessRatio
from .n_subjettiness_ratio import TauMN
from .observable import PHYSICS_OBJECT_OPTIONS
from .observable import Observable
from .observable import PhysicsObjectOptions


def get(identifier: str | None, *arg, **kwarg):
    if identifier == "" or identifier is None:
        return None

    if "." in identifier:
        physics_object, name = identifier.split(".")
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
