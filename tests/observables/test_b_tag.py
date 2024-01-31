from math import isnan

from hml.observables.b_tag import BTag


def test_init():
    obs = BTag(physics_object="FatJet0")

    # Parameters ------------------------------------------------------------- #
    assert obs.physics_object.name == "FatJet0"
    assert obs.supported_types == ["single", "collective"]

    # Attributes ------------------------------------------------------------- #
    assert obs.name == "FatJet0.BTag"
    assert isnan(obs.value)
    assert obs.shape == "1 * float64"
    assert obs.config == {"physics_object": obs.physics_object.name}
    assert repr(obs) == "FatJet0.BTag : nan"


def test_class_methods():
    obs = BTag(physics_object="FatJet0")
    assert obs == BTag.from_name("FatJet0.BTag")
    assert obs == BTag.from_config(obs.config)


def test_read(event):
    obs = BTag("FatJet0").read_ttree(event)
    assert obs.shape == "1 * float64"

    obs = BTag("FatJet:5").read_ttree(event)
    assert obs.shape == "5 * float64"
