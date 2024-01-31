from math import isnan

from hml.observables.dummy import Dummy


def test_init():
    obs = Dummy()

    # Parameters ------------------------------------------------------------- #
    assert obs.physics_object is None
    assert obs.supported_types is None

    # Attributes ------------------------------------------------------------- #
    assert obs.name == "Dummy"
    assert isnan(obs.value)
    assert obs.shape == "1 * float64"
    assert obs.config == {}


def test_class_methods():
    obs = Dummy()

    assert repr(obs) == "Dummy : nan"
    assert obs == Dummy.from_name("Dummy")
    assert obs == Dummy.from_config(obs.config)


def test_read(event):
    obs = Dummy("Jet0").read_ttree(event)
    assert obs.shape == "1 * float64"

    obs = Dummy("Jet:5").read_ttree(event)
    assert obs.shape == "1 * float64"

    obs = Dummy("Jet:2.Constituents:5").read_ttree(event)
    assert obs.shape == "1 * float64"
