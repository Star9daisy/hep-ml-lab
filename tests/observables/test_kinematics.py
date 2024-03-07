import awkward as ak
import pytest

from hml import physics_objects
from hml.observables import kinematics


def test_init():
    obs = kinematics.Pt(physics_object="jet0")

    assert obs.physics_object.name == "jet0"
    assert obs.class_name == "Pt"

    assert obs.name == "jet0.Pt"
    assert len(obs.value) == 0
    assert obs.config == {"physics_object": "jet0", "class_name": "Pt"}

    # Other initializations
    assert kinematics.Pt(physics_object=physics_objects.parse("jet0")).name == "jet0.Pt"
    assert kinematics.Pt(physics_object="jet0", class_name="pt").name == "jet0.pt"

    assert kinematics.Px(physics_object="jet0").name == "jet0.Px"
    assert kinematics.Py(physics_object="jet0").name == "jet0.Py"
    assert kinematics.Pz(physics_object="jet0").name == "jet0.Pz"
    assert kinematics.E(physics_object="jet0").name == "jet0.E"
    assert kinematics.Eta(physics_object="jet0").name == "jet0.Eta"
    assert kinematics.Phi(physics_object="jet0").name == "jet0.Phi"
    assert kinematics.M(physics_object="jet0").name == "jet0.M"


def test_special_methods():
    obs = kinematics.Pt(physics_object="jet0")

    assert obs == kinematics.Pt(physics_object="jet0")
    assert obs == "jet0.pt"
    assert obs == "Jet0.transverse_momentum"
    assert str(obs) == "jet0.Pt: 0 * unknown"
    assert repr(obs) == "jet0.Pt: 0 * unknown"


def test_class_methods():
    obs = kinematics.Pt(physics_object="jet0")

    assert kinematics.Pt.from_name("jet0.Pt").name == "jet0.Pt"
    assert kinematics.Pt.from_config(obs.config).name == "jet0.Pt"

    with pytest.raises(ValueError):
        kinematics.Pt.from_name("jet0,jet1")


def test_read(events):
    cut = events["Jet_size"].array() > 0

    obs = kinematics.Pt(physics_object="jet0").read(events)
    assert ak.all(obs.value[cut][:, 0] == events["Jet.PT"].array()[cut][:, 0])

    obs = kinematics.Pt(physics_object="jet.constituents").read(events)
    assert str(obs.value.type) == f"{ak.sum(cut)} * var * var * float32"

    obs = kinematics.Pt(physics_object="jet:10.constituents:100").read(events)
    assert str(obs.value.type) == f"{ak.sum(cut)} * 10 * 100 * ?float32"

    obs = kinematics.Px(physics_object="jet0").read(events)
    assert str(obs.value.type) == f"{ak.sum(cut)} * 1 * float32"
