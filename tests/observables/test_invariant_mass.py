import pytest

from hml.observables import InvariantMass


def test_init():
    obs = InvariantMass(physics_object="jet0,jet1")

    assert obs.physics_object.name == "jet0,jet1"
    assert obs.class_name == "InvariantMass"

    assert obs.name == "jet0,jet1.InvariantMass"
    assert len(obs.value) == 0
    assert obs.config == {
        "physics_object": obs.physics_object.name,
        "class_name": "InvariantMass",
    }


def test_special_methods():
    obs = InvariantMass(physics_object="jet0,jet1")

    assert obs == InvariantMass(physics_object="jet0,jet1")
    assert obs == "jet0,jet1.InvariantMass"
    assert obs == "jet0,jet1.invariant_mass"
    assert str(obs) == "jet0,jet1.InvariantMass: 0 * unknown"
    assert repr(obs) == "jet0,jet1.InvariantMass: 0 * unknown"


def test_class_methods():
    obs = InvariantMass(physics_object="jet0,jet1")

    assert obs == InvariantMass.from_name("jet0,jet1.InvariantMass")
    assert obs == InvariantMass.from_config(obs.config)

    with pytest.raises(ValueError):
        InvariantMass.from_name("jet,muon")


def test_read(events):
    obs = InvariantMass("jet0,jet1").read(events)
    assert str(obs.value.type) == "100 * 1 * ?float32"

    obs = InvariantMass("jet0,jet1,jet2").read(events)
    assert str(obs.value.type) == "100 * 1 * ?float32"

    obs = InvariantMass("jet0,jet1,jet100").read(events)
    assert str(obs.value.type) == "100 * 1 * ?float32"
