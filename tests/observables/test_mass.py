from math import isnan

from hml.observables.mass import M
from hml.observables.mass import Mass


def test_init():
    obs = Mass(physics_object="Jet0")

    # Parameters ------------------------------------------------------------- #
    assert obs.physics_object.name == "Jet0"
    assert obs.supported_types == ["single", "collective", "nested"]

    # Attributes ------------------------------------------------------------- #
    assert obs.name == "Jet0.Mass"
    assert isnan(obs.value)
    assert obs.shape == "1 * float64"
    assert obs.config == {"physics_object": obs.physics_object.name}


def test_class_methods():
    obs = Mass(physics_object="Jet0")

    assert repr(obs) == "Jet0.Mass : nan"
    assert obs == Mass.from_name("Jet0.Mass")


def test_read(event):
    obs = M("Jet0").read_ttree(event)
    assert obs.shape == "1 * float64"

    obs = M("Jet:5").read_ttree(event)
    assert obs.shape == "5 * float64"

    obs = M("Jet:2.Constituents:5").read_ttree(event)
    assert obs.shape == "2 * 5 * float64"
