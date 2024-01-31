from math import isnan

from hml.observables.tau_tag import TauTag


def test_init():
    obs = TauTag(physics_object="FatJet0")

    # Parameters ------------------------------------------------------------- #
    assert obs.physics_object.name == "FatJet0"
    assert obs.supported_types == ["single", "collective"]

    # Attributes ------------------------------------------------------------- #
    assert obs.name == "FatJet0.TauTag"
    assert isnan(obs.value)
    assert obs.shape == "1 * float64"
    assert obs.config == {"physics_object": obs.physics_object.name}
    assert repr(obs) == "FatJet0.TauTag : nan"


def test_class_methods():
    obs = TauTag(physics_object="FatJet0")
    assert obs == TauTag.from_name("FatJet0.TauTag")
    assert obs == TauTag.from_config(obs.config)


def test_read(event):
    obs = TauTag("FatJet0").read_ttree(event)
    assert obs.shape == "1 * float64"

    obs = TauTag("FatJet:5").read_ttree(event)
    assert obs.shape == "5 * float64"
