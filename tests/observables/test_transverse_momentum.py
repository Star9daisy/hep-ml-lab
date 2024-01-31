from math import isnan

from hml.observables.transverse_momentum import Pt
from hml.observables.transverse_momentum import TransverseMomentum


def test_init():
    obs = TransverseMomentum(physics_object="Jet0")

    # Parameters ------------------------------------------------------------- #
    assert obs.physics_object.name == "Jet0"
    assert obs.supported_types == ["single", "collective", "nested"]

    # Attributes ------------------------------------------------------------- #
    assert obs.name == "Jet0.TransverseMomentum"
    assert isnan(obs.value)
    assert obs.shape == "1 * float64"
    assert obs.config == {"physics_object": obs.physics_object.name}


def test_class_methods():
    obs = TransverseMomentum(physics_object="Jet0")

    assert repr(obs) == "Jet0.TransverseMomentum : nan"
    assert obs == TransverseMomentum.from_name("Jet0.TransverseMomentum")


def test_read(event):
    obs = Pt("Jet0").read_ttree(event)
    assert obs.shape == "1 * float64"

    obs = Pt("Jet:5").read_ttree(event)
    assert obs.shape == "5 * float64"

    obs = Pt("Jet:2.Constituents:5").read_ttree(event)
    assert obs.shape == "2 * 5 * float64"
