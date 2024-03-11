import pytest

from hml.observables.angular_distance import AngularDistance


def test_attributes():
    obs = AngularDistance(physics_object="Jet0,Jet1")

    assert obs.physics_object.name == "Jet0,Jet1"
    assert obs.class_name == "AngularDistance"

    assert obs.name == "Jet0,Jet1.AngularDistance"
    assert len(obs.value) == 0
    assert obs.config == {
        "physics_object": obs.physics_object.name,
        "class_name": "AngularDistance",
    }


def test_class_methods():
    obs = AngularDistance(physics_object="Jet0,Jet1")

    assert obs == AngularDistance.from_name("Jet0,Jet1.AngularDistance")
    assert obs == AngularDistance.from_config(obs.config)

    with pytest.raises(AssertionError):
        AngularDistance(physics_object="Jet0,Jet1,Jet2")


def test_read(events):
    obj = AngularDistance("Jet0,Jet1").read(events)
    assert str(obj.value.type) == "100 * 1 * 1 * ?float32"

    obj = AngularDistance("Jet0,Jet1.Constituents100:").read(events)
    assert str(obj.value.type) == "100 * 1 * 0 * float32"

    obj = AngularDistance("Jet:5,Jet:5").read(events)
    assert str(obj.value.type) == "100 * 5 * 5 * ?float32"

    obj = AngularDistance("Jet0.Constituents:10,Jet1.Constituents:10").read(events)
    assert str(obj.value.type) == "100 * 10 * 10 * ?float32"
