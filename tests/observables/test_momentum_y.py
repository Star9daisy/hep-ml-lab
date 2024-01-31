from math import isnan

from hml.observables.momentum_y import MomentumY
from hml.observables.momentum_y import Py


def test_init():
    obs = MomentumY(physics_object="Jet0")

    # Parameters ------------------------------------------------------------- #
    assert obs.physics_object.name == "Jet0"
    assert obs.supported_types == ["single", "collective", "nested"]

    # Attributes ------------------------------------------------------------- #
    assert obs.name == "Jet0.MomentumY"
    assert isnan(obs.value)
    assert obs.shape == "1 * float64"
    assert obs.config == {"physics_object": obs.physics_object.name}


def test_class_methods():
    obs = MomentumY(physics_object="Jet0")

    assert repr(obs) == "Jet0.MomentumY : nan"
    assert obs == MomentumY.from_name("Jet0.MomentumY")


def test_read(event):
    obs = Py("Jet0").read_ttree(event)
    assert obs.shape == "1 * float64"

    obs = Py("Jet:5").read_ttree(event)
    assert obs.shape == "5 * float64"

    obs = Py("Jet:2.Constituents:5").read_ttree(event)
    assert obs.shape == "2 * 5 * float64"
