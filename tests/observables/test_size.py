from math import isnan

from hml.observables.size import Size


def test_init():
    obs = Size(physics_object="FatJet:")

    # Parameters ------------------------------------------------------------- #
    assert obs.physics_object.name == "FatJet:"
    assert obs.supported_types == ["collective"]

    # Attributes ------------------------------------------------------------- #
    assert obs.name == "FatJet:.Size"
    assert isnan(obs.value)
    assert obs.shape == "1 * float64"
    assert obs.config == {"physics_object": obs.physics_object.name}
    assert repr(obs) == "FatJet:.Size : nan"


def test_class_methods():
    obs = Size(physics_object="FatJet:")
    assert obs == Size.from_name("FatJet:.Size")
    assert obs == Size.from_config(obs.config)


def test_read(event):
    obs = Size("FatJet:").read_ttree(event)
    assert obs.shape == "1 * float64"

    obs = Size("FatJet:5").read_ttree(event)
    assert obs.shape == "1 * float64"
