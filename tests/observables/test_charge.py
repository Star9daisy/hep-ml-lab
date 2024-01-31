from math import isnan

from hml.observables.charge import Charge


def test_init():
    obs = Charge(physics_object="FatJet0")

    # Parameters ------------------------------------------------------------- #
    assert obs.physics_object.name == "FatJet0"
    assert obs.supported_types == ["single", "collective"]

    # Attributes ------------------------------------------------------------- #
    assert obs.name == "FatJet0.Charge"
    assert isnan(obs.value)
    assert obs.shape == "1 * float64"
    assert obs.config == {"physics_object": obs.physics_object.name}
    assert repr(obs) == "FatJet0.Charge : nan"


def test_class_methods():
    obs = Charge(physics_object="FatJet0")
    assert obs == Charge.from_name("FatJet0.Charge")
    assert obs == Charge.from_config(obs.config)


def test_read(event):
    obs = Charge("FatJet0").read_ttree(event)
    assert obs.shape == "1 * float64"

    obs = Charge("FatJet:5").read_ttree(event)
    assert obs.shape == "5 * float64"
