from math import isnan

from hml.observables.pseudo_rapidity import Eta
from hml.observables.pseudo_rapidity import PseudoRapidity


def test_init():
    obs = PseudoRapidity(physics_object="Jet0")

    # Parameters ------------------------------------------------------------- #
    assert obs.physics_object.name == "Jet0"
    assert obs.supported_types == ["single", "collective", "nested"]

    # Attributes ------------------------------------------------------------- #
    assert obs.name == "Jet0.PseudoRapidity"
    assert isnan(obs.value)
    assert obs.shape == "1 * float64"
    assert obs.config == {"physics_object": obs.physics_object.name}


def test_class_methods():
    obs = PseudoRapidity(physics_object="Jet0")

    assert repr(obs) == "Jet0.PseudoRapidity : nan"
    assert obs == PseudoRapidity.from_name("Jet0.PseudoRapidity")


def test_read(event):
    obs = Eta("Jet0").read_ttree(event)
    assert obs.shape == "1 * float64"

    obs = Eta("Jet:5").read_ttree(event)
    assert obs.shape == "5 * float64"

    obs = Eta("Jet:2.Constituents:5").read_ttree(event)
    assert obs.shape == "2 * 5 * float64"
