import awkward as ak
import pytest

from hml.observables import BTag, Charge, TauTag


def test_init():
    obs = Charge(physics_object="jet0")

    assert obs.physics_object.name == "jet0"
    assert obs.class_name == "Charge"

    assert obs.name == "jet0.Charge"
    assert len(obs.value) == 0
    assert obs.config == {"physics_object": "jet0", "class_name": "Charge"}

    with pytest.raises(ValueError):
        Charge(physics_object="jet0.constituents")

    # Other initializations
    assert BTag(physics_object="jet0").name == "jet0.BTag"
    assert TauTag(physics_object="jet0").name == "jet0.TauTag"


def test_read(events):
    obs = Charge(physics_object="jet").read(events)
    assert ak.all(obs.value == events["Jet.Charge"].array())

    obs = BTag(physics_object="jet").read(events)
    assert ak.all(obs.value == events["Jet.BTag"].array())

    obs = TauTag(physics_object="jet").read(events)
    assert ak.all(obs.value == events["Jet.TauTag"].array())
