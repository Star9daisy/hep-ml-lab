from math import isnan

from hml.observables.energy import E
from hml.observables.energy import Energy


def test_init():
    obs = Energy(physics_object="Jet0")

    # Parameters ------------------------------------------------------------- #
    assert obs.physics_object.name == "Jet0"
    assert obs.supported_types == ["single", "collective", "nested"]

    # Attributes ------------------------------------------------------------- #
    assert obs.name == "Jet0.Energy"
    assert isnan(obs.value)
    assert obs.shape == "1 * float64"
    assert obs.config == {"physics_object": obs.physics_object.name}


def test_class_methods():
    obs = Energy(physics_object="Jet0")

    assert repr(obs) == "Jet0.Energy : nan"
    assert obs == Energy.from_name("Jet0.Energy")


def test_read(event):
    obs = E("Jet0").read_ttree(event)
    assert obs.shape == "1 * float64"

    obs = E("Jet:5").read_ttree(event)
    assert obs.shape == "5 * float64"

    obs = E("Jet:2.Constituents:5").read_ttree(event)
    assert obs.shape == "2 * 5 * float64"
