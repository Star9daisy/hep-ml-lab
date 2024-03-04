from .observable import Observable


class Px(Observable): ...


class Py(Observable): ...


class Pz(Observable): ...


class E(Observable): ...


class Pt(Observable): ...


class Eta(Observable): ...


class Phi(Observable): ...


class M(Observable): ...


Px.add_alias("px", "MomentumX", "momentum_x")
Py.add_alias("py", "MomentumY", "momentum_y")
Pz.add_alias("pz", "MomentumZ", "momentum_z")
E.add_alias("e", "Energy", "energy")

Pt.add_alias("pt", "PT", "pT", "TransverseMomentum", "transverse_momentum")
Eta.add_alias("eta", "PseudoRapidity", "pseudo_rapidity")
Phi.add_alias("phi", "AzimuthalAngle", "azimuthal_angle")
M.add_alias("m", "Mass", "mass")
