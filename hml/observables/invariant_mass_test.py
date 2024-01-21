from math import isnan

import pytest

from ..events.delphes_events import DelphesEvents
from ..observables.invariant_mass import InvariantMass
from ..observables.invariant_mass import InvM
from ..observables.invariant_mass import InvMass


@pytest.fixture
def event():
    events = DelphesEvents("tests/data/pp2zz/Events/run_01/tag_1_delphes_events.root")
    yield events[0]


def test_invariant_mass(event):
    obs = InvariantMass(physics_object="Jet0,Jet1")
    assert obs.physics_object.name == "Jet0,Jet1"
    assert obs.supported_objects == ["single", "multiple"]
    assert obs.name == "InvariantMass"
    assert isnan(obs.value)
    assert obs.fullname == "Jet0,Jet1.InvariantMass"
    assert repr(obs) == f"{obs.fullname}: {obs.value}"
    assert obs.classname == "InvariantMass"
    assert obs.config == {
        "physics_object": "Jet0,Jet1",
        "name": None,
        "value": None,
        "supported_objects": ["single", "multiple"],
    }
    assert InvariantMass.from_name("Jet0,Jet1.InvariantMass").fullname == obs.fullname
    assert InvariantMass.from_config(obs.config).fullname == obs.fullname

    obs.read(event)
    assert isinstance(obs.value, float)


def test_inv_mass(event):
    obs = InvMass(physics_object="Jet0,Jet1")
    assert obs.physics_object.name == "Jet0,Jet1"
    assert obs.supported_objects == ["single", "multiple"]
    assert obs.name == "InvMass"
    assert isnan(obs.value)
    assert obs.fullname == "Jet0,Jet1.InvMass"
    assert repr(obs) == f"{obs.fullname}: {obs.value}"
    assert obs.classname == "InvMass"
    assert obs.config == {
        "physics_object": "Jet0,Jet1",
        "name": None,
        "value": None,
        "supported_objects": ["single", "multiple"],
    }
    assert InvMass.from_name("Jet0,Jet1.InvMass").fullname == obs.fullname
    assert InvMass.from_config(obs.config).fullname == obs.fullname

    obs.read(event)
    assert isinstance(obs.value, float)


def test_inv_m(event):
    obs = InvM(physics_object="Jet0,Jet1")
    assert obs.physics_object.name == "Jet0,Jet1"
    assert obs.supported_objects == ["single", "multiple"]
    assert obs.name == "InvM"
    assert isnan(obs.value)
    assert obs.fullname == "Jet0,Jet1.InvM"
    assert repr(obs) == f"{obs.fullname}: {obs.value}"
    assert obs.classname == "InvM"
    assert obs.config == {
        "physics_object": "Jet0,Jet1",
        "name": None,
        "value": None,
        "supported_objects": ["single", "multiple"],
    }
    assert InvM.from_name("Jet0,Jet1.InvM").fullname == obs.fullname
    assert InvM.from_config(obs.config).fullname == obs.fullname

    obs.read(event)
    assert isinstance(obs.value, float)


def bad_case(event):
    # Unsupported physics object
    with pytest.raises(ValueError):
        InvariantMass(physics_object="Jet0.Particles")

    # Too big index
    assert InvariantMass(physics_object="Jet100,Jet1").value == event.Jet1.Mass
    assert InvariantMass(physics_object="Jet100,Jet100").value == 0
