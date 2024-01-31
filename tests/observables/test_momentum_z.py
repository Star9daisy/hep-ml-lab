from math import isnan

from hml.observables.momentum_z import MomentumZ
from hml.observables.momentum_z import Pz


def test_init():
    obs = MomentumZ(physics_object="Jet0")

    # Parameters ------------------------------------------------------------- #
    assert obs.physics_object.name == "Jet0"
    assert obs.supported_types == ["single", "collective", "nested"]

    # Attributes ------------------------------------------------------------- #
    assert obs.name == "Jet0.MomentumZ"
    assert isnan(obs.value)
    assert obs.shape == "1 * float64"
    assert obs.config == {"physics_object": obs.physics_object.name}


def test_class_methods():
    obs = MomentumZ(physics_object="Jet0")

    assert repr(obs) == "Jet0.MomentumZ : nan"
    assert obs == MomentumZ.from_name("Jet0.MomentumZ")


def test_read(event):
    obs = Pz("Jet0").read_ttree(event)
    assert obs.shape == "1 * float64"

    obs = Pz("Jet:5").read_ttree(event)
    assert obs.shape == "5 * float64"

    obs = Pz("Jet:2.Constituents:5").read_ttree(event)
    assert obs.shape == "2 * 5 * float64"
