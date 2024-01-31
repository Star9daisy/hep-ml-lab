from math import isnan

from hml.observables.momentum_x import MomentumX
from hml.observables.momentum_x import Px


def test_init():
    obs = MomentumX(physics_object="Jet0")

    # Parameters ------------------------------------------------------------- #
    assert obs.physics_object.name == "Jet0"
    assert obs.supported_types == ["single", "collective", "nested"]

    # Attributes ------------------------------------------------------------- #
    assert obs.name == "Jet0.MomentumX"
    assert isnan(obs.value)
    assert obs.shape == "1 * float64"
    assert obs.config == {"physics_object": obs.physics_object.name}


def test_class_methods():
    obs = MomentumX(physics_object="Jet0")

    assert repr(obs) == "Jet0.MomentumX : nan"
    assert obs == MomentumX.from_name("Jet0.MomentumX")


def test_read(event):
    obs = Px("Jet0").read_ttree(event)
    assert obs.shape == "1 * float64"

    obs = Px("Jet:5").read_ttree(event)
    assert obs.shape == "5 * float64"

    obs = Px("Jet:2.Constituents:5").read_ttree(event)
    assert obs.shape == "2 * 5 * float64"
